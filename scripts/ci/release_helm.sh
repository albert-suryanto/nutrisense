#! /bin/sh
# rm .git/hooks/*
npm install conventional-changelog-conventionalcommits@6.1.0
sg release || true
