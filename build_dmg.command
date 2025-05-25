#!/bin/bash
hdiutil create -volname EasySee \
  -srcfolder dist/main.app \
  -ov -format UDZO EasySee.dmg
