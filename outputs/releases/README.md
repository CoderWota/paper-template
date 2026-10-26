# Releases

Preserved output packages, such as the exact files submitted to a journal for one round. One subdirectory per release: `<release-id>/`. A release is frozen once created, and later rebuilds never overwrite it.

## Each release records

- The delivered files: manuscript, figures, supplements, and other required material.
- A README written before freezing: what the release is for, when it was made, and its validation result.
- Checksums of the manuscript and inputs, the profile revision, bibliography, assets, tool versions, the build command, and validation results, so that the package can be traced and reproduced.

A release is not automatically approved or submitted. Approval and submission are your separate decisions.

## Who edits what

The agent creates a release when you ask for a final package. Do not edit a release; make a new one instead.
