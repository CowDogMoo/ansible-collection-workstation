//go:build mage

package main

import (
	"fmt"
	"os"

	"github.com/bitfield/script"
	"github.com/fatih/color"
	"github.com/l50/goutils/v2/dev/lint"
	mageutils "github.com/l50/goutils/v2/dev/mage"
	"github.com/l50/goutils/v2/sys"
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
		"ansible-lint --force-color -c .hooks/linters/.ansible-lint.yaml",
	}

	fmt.Println(color.YellowString("Running ansible-lint."))
	if err := runCmds(cmds); err != nil {
		return fmt.Errorf(color.RedString("failed to run ansible-lint: %v", err))
	}

	return nil
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
	cmds := []string{
		"molecule test",
	}

	fmt.Println(color.YellowString("Running molecule tests."))
	if err := runCmds(cmds); err != nil {
		return fmt.Errorf(color.RedString("failed to run molecule tests: %v", err))
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
	if err := runCmds(cmds); err != nil {
		return fmt.Errorf(color.RedString("failed to generate changelog: %v", err))
	}

	return nil
}
