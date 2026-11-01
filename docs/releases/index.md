# Releases

A Hopsworks release is numbered X.Y.Z, the version of its Helm chart.
A minor release is numbered X.Y.0, such as 5.2.0.
A patch release is numbered X.Y.Z with Z above 0, such as 5.2.1.

A patch release lists what changed since the previous release of its minor version, so 5.1.2 lists what changed since 5.1.1, and 5.2.1 what changed since 5.2.0.
A minor release lists everything since the previous minor release, so 5.2.0 lists everything since 5.1.0, and marks the changes that already shipped in a patch release of 5.1.

When you upgrade, read the breaking changes of every release between yours and the one you upgrade to, and follow the upgrade steps of each release on the way.

<!-- releases -->
