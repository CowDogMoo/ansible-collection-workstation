# Molecule Tests for Fabric Role

This directory contains Molecule tests for the `fabric` role, specifically testing the idempotent behavior of managing `~/.default-golang-pkgs`.

## Test Scenarios

### 1. Fresh Installation (`ubuntu-fabric-fresh`)

Tests the behavior when `~/.default-golang-pkgs` doesn't exist:

- ✅ File should be created
- ✅ Fabric package should be added
- ✅ Header comment should be added
- ✅ Only Fabric should be present

### 2. Existing Packages (`ubuntu-fabric-existing`)

Tests the behavior when the file exists with other Go packages (but not Fabric):

- ✅ Existing packages should be preserved
- ✅ Fabric should be added
- ✅ No packages should be removed

### 3. Fabric Already Present (`ubuntu-fabric-present`)

Tests the behavior when Fabric is already in the file:

- ✅ Fabric should NOT be duplicated
- ✅ Existing packages should be preserved
- ✅ No changes should be made (idempotent)

### 4. Idempotency Test

All scenarios run the role twice:

- ✅ Second run should report no changes
- ✅ File content should remain the same

## Running the Tests

```bash
# Run all tests
cd roles/fabric
molecule test

# Run individual steps
molecule create      # Create test containers
molecule prepare     # Set up test scenarios
molecule converge    # Apply the role
molecule verify      # Run verification tests
molecule destroy     # Clean up

# Debug mode
molecule converge -- -vvv
```

## Expected Outcomes

All tests should pass, demonstrating that:

1. The role safely adds Fabric to `~/.default-golang-pkgs`
2. Existing packages are never overwritten or removed
3. Fabric is never duplicated
4. The role is fully idempotent
