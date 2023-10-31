//go:build mage
// +build mage

package main

import (
	"fmt"
	"os"
	"path/filepath"
	"sync"

	"github.com/bitfield/script"
	"github.com/fatih/color"
	"github.com/l50/goutils/v2/dev/lint"
	mageutils "github.com/l50/goutils/v2/dev/mage"
	"github.com/l50/goutils/v2/docs"
	"github.com/l50/goutils/v2/git"
	"github.com/l50/goutils/v2/sys"
	"github.com/spf13/afero"
)

func init() {
	os.Setenv("GO111MODULE", "on")
}

// InstallDeps installs the Go dependencies necessary for developing
// on the project.
//
// Example usage:
//
// ```go
// mage installdeps
// ```
//
// **Returns:**
//
// error: An error if any issue occurs while trying to
// install the dependencies.
func InstallDeps() error {
	fmt.Println("Installing dependencies.")

	cwd := sys.Gwd()
	if err := sys.Cd("magefiles"); err != nil {
		return fmt.Errorf("failed to cd into magefiles directory: %v", err)
	}

	if err := mageutils.Tidy(); err != nil {
		return fmt.Errorf("failed to install dependencies: %v", err)
	}

	if err := sys.Cd(cwd); err != nil {
		return fmt.Errorf("failed to cd into project root directory: %v", err)
	}

	if err := lint.InstallGoPCDeps(); err != nil {
		return fmt.Errorf("failed to install pre-commit dependencies: %v", err)
	}

	if err := mageutils.InstallVSCodeModules(); err != nil {
		return fmt.Errorf("failed to install vscode-go modules: %v", err)
	}

	return nil
}

// RunPreCommit updates, clears, and executes all pre-commit hooks
// locally. The function follows a three-step process:
//
// First, it updates the pre-commit hooks.
// Next, it clears the pre-commit cache to ensure a clean environment.
// Lastly, it executes all pre-commit hooks locally.
//
// Example usage:
//
// ```go
// mage runprecommit
// ```
//
// **Returns:**
//
// error: An error if any issue occurs at any of the three stages
// of the process.
func RunPreCommit() error {
	fmt.Println("Updating pre-commit hooks.")
	if err := lint.UpdatePCHooks(); err != nil {
		return err
	}

	fmt.Println("Clearing the pre-commit cache to ensure we have a fresh start.")
	if err := lint.ClearPCCache(); err != nil {
		return err
	}

	fmt.Println("Running all pre-commit hooks locally.")
	if err := lint.RunPCHooks(); err != nil {
		return err
	}

	return nil
}

func runCmds(cmds []string) error {
	for _, cmd := range cmds {
		if _, err := script.Exec(cmd).Stdout(); err != nil {
			return err
		}
	}

	return nil

}

// LintAnsible runs the ansible-lint linter.
//
// Example usage:
//
// ```bash
// mage lintansible
// ```
//
// **Returns:**
//
// error: An error if any issue occurs while trying to run the linter.
func LintAnsible() error {
	cmds := []string{
		"ansible-lint --force-color -c .hooks/linters/ansible-lint.yaml",
	}

	fmt.Println(color.YellowString("Running ansible-lint."))
	return runCmds(cmds)
}

// RunMoleculeTests runs the molecule tests.
//
// Example usage:
//
// ```bash
// mage runmoleculetests
// ```
//
// **Returns:**
//
// error: An error if any issue occurs while trying to run the tests.
func RunMoleculeTests() error {
	fs := afero.NewOsFs() // Create a new Afero FS instance for file system operations
	rolesDir := "roles"

	// List all the roles in the roles directory
	roles, err := afero.ReadDir(fs, rolesDir)
	if err != nil {
		return fmt.Errorf("failed to list roles: %v", err)
	}

	cmds := []string{
		"molecule test",
	}

	// Print all of the roles before running the tests
	fmt.Println(color.YellowString("Running molecule tests for the following roles:"))
	fmt.Println(color.YellowString("=============================================="))

	// Create a channel to collect errors from goroutines
	errCh := make(chan error, len(roles))
	// Create a wait group to wait for all goroutines to complete
	var wg sync.WaitGroup

	for _, role := range roles {
		if !role.IsDir() {
			continue // Skip any non-directory files
		}

		wg.Add(1) // Increment the wait group counter
		go func(role os.FileInfo) {
			defer wg.Done() // Decrement the counter when the goroutine completes

			rolePath := filepath.Join(rolesDir, role.Name())
			fmt.Printf(color.YellowString("Running molecule tests for the %s role\n"), role.Name())

			cwd := sys.Gwd()

			// Change to the role's directory
			if err := sys.Cd(rolePath); err != nil {
				errCh <- fmt.Errorf("failed to cd into %s role directory: %v", role.Name(), err)
				return
			}

			if err := runCmds(cmds); err != nil {
				errCh <- fmt.Errorf("failed to run molecule tests for role %s: %v", role.Name(), err)
			}

			// Change back to the original directory
			if err := sys.Cd(cwd); err != nil {
				errCh <- fmt.Errorf("failed to cd out of %s role directory: %v", role.Name(), err)
			}
		}(role) // Pass the role to the goroutine
	}

	wg.Wait() // Wait for all goroutines to complete

	close(errCh) // Close the error channel

	// Collect any errors from the channel
	var errors []error
	for err := range errCh {
		errors = append(errors, err)
	}

	if len(errors) > 0 {
		return fmt.Errorf("encountered errors: %v", errors)
	}

	return nil
}

// GenChangeLog generates the changelog used by Ansible Galaxy.
//
// Example usage:
//
// ```bash
// mage genchangelog
// ```
//
// **Returns:**
//
// error: An error if any issue occurs while trying to generate the changelog.
func GenChangeLog() error {
	cmds := []string{
		"antsibull-changelog lint",
		"antsibull-changelog release",
	}

	fmt.Println(color.YellowString("Generating changelog"))
	return runCmds(cmds)
}

// CreateRelease creates a release on GitHub.
//
// **Parameters:**
//
// version: A string representing the version to use for the release.
//
// Example usage:
//
// ```bash
// NEXT_VERSION=1.0.0 mage createrelease
// ```
//
// **Returns:**
//
// error: An error if any issue occurs while trying to create the release.
func CreateRelease() error {
	// Check for the presence of the 'release' environment variable
	version, ok := os.LookupEnv("NEXT_VERSION")
	if !ok {
		return fmt.Errorf("'NEXT_VERSION' environment variable not set. \n" +
			"Example: NEXT_VERSION=1.0.0 mage createrelease")
	}

	cmds := []string{
		"gh release create " + version + " -F " + filepath.Join("changelogs", "CHANGELOG.rst"),
	}

	fmt.Printf(color.YellowString("Creating release %s\n", version))
	return runCmds(cmds)
}

// GeneratePackageDocs creates documentation for the various packages
// in the project.
//
// Example usage:
//
// ```go
// mage generatepackagedocs
// ```
//
// **Returns:**
//
// error: An error if any issue occurs during documentation generation.
func GeneratePackageDocs() error {
	fs := afero.NewOsFs()

	repoRoot, err := git.RepoRoot()
	if err != nil {
		return fmt.Errorf("failed to get repo root: %v", err)
	}
	sys.Cd(repoRoot)

	repo := docs.Repo{
		Owner: "CowDogMoo",
		Name:  "ansible-collection-workstation",
	}

	templatePath := filepath.Join("magefiles", "tmpl", "README.md.tmpl")
	if err := docs.CreatePackageDocs(fs, repo, templatePath); err != nil {
		return fmt.Errorf("failed to create package docs: %v", err)
	}

	return nil
}
