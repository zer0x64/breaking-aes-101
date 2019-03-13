#!/bin/bash

~/.cargo/bin/wasm-pack build --no-typescript --release --out-dir ../website/wasm/ --target no-modules

#cargo +nightly build --target=wasm32-unknown-unknown --release
#~/.cargo/bin/wasm-bindgen --no-modules --no-modules-global cbc3 --no-typescript --out-dir ../website/wasm/ target/wasm32-unknown-unknown/release/cbc3_wasm.wasm
