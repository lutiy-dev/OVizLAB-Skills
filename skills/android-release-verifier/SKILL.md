---
name: android-release-verifier
description: Audit Android APK release readiness across Gradle, CI, signing continuity, in-place update compatibility and real-device QA.
---
# Android Release Verifier
## Trigger
Use for Android APK, GitHub Actions build, Play/side-load release and in-place update verification.
## Inputs
Repository, baseline installed version/versionCode/package identifier, target commit/tag, keystore continuity evidence, current CI run, phone/TV QA.
## Procedure
1. Read repository policies, Gradle manifests, package/applicationId, versionName/versionCode, signing configs and release workflows. Never print signing secrets.
2. Verify the candidate is built from intended main/tag SHA, not a stale branch. Check CI logs, artifact checksums and release asset names.
3. Compare applicationId and versionCode with installed baseline. A higher versionCode and matching ID are necessary but not sufficient for an in-place update.
4. Verify signing certificate identity across old and new APK using available trustworthy fingerprints; if APKs/keys are unavailable, state NOT CONFIRMED. Do not generate replacement signing keys.
5. Verify installation over prior version, retained settings/auth/data and successful launch on Phone and Android TV separately, only when devices or authorized test runners are available.
6. Check playback/network failure behavior, remote/D-pad, search, back navigation, updates and downgrade/rollback constraints when in scope.
7. Document provenance, SHA-256, PR/release URL, PASS/FAIL/NOT CONFIRMED matrix, and recovery steps.
## Acceptance
BUILD PASS does not equal UPDATE PASS. UPDATE PASS requires actual compatible signed APK and verified in-place installation; DEVICE PASS requires actual device tests.
## STOP
Unverified signing continuity, unexpected app ID, non-increasing versionCode, secrets exposure, update that wipes data, or unauthorized release publication.
