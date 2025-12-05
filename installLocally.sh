#!/bin/sh

rm -rf /tmp/kotlin-sdk
git clone https://github.com/steviec/kotlin-sdk.git /tmp/kotlin-sdk

./gradlew :maestro-android:assembleDebug :maestro-android:assembleAndroidTest :maestro-cli:installDist

rm -rf ~/.maestro/bin
rm -rf ~/.maestro/lib

cp -r ./maestro-cli/build/install/maestro/bin ~/.maestro/bin
cp -r ./maestro-cli/build/install/maestro/lib ~/.maestro/lib