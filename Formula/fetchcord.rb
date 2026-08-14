# typed: strict
# frozen_string_literal: true

# Homebrew formula for FetchCord.
#
# To install from a Homebrew tap (a repo named `fetchcord/homebrew-fetchcord`
# that contains this file under `Formula/`):
#
#   brew tap fetchcord/homebrew-fetchcord
#   brew install fetchcord
#
# To test it locally without a tap:
#
#   brew install --build-from-source ./Formula/fetchcord.rb
#
# At every release, update `url` to the new tag and set `sha256` to the
# tarball's checksum:
#
#   curl -Ls https://github.com/fetchcord/FetchCord/archive/refs/tags/vX.Y.Z.tar.gz | shasum -a 256

class Fetchcord < Formula
  desc "Display system information as Discord Rich Presence"
  homepage "https://github.com/fetchcord/FetchCord"
  url "https://github.com/fetchcord/FetchCord/archive/refs/tags/v3.0.0.tar.gz"
  sha256 "REPLACE_WITH_RELEASE_TARBALL_SHA256"
  license "MIT"

  depends_on "python@3.12"
  depends_on "fastfetch"

  def install
    # Installs fetchcord and its Python dependencies into the formula prefix.
    system "python3", "-m", "pip", "install", ".", "--prefix", libexec
    bin.install_symlink libexec/"bin/fetchcord"
  end

  test do
    assert_match "FetchCord version:", shell_output("#{bin}/fetchcord --version")
  end

  livecheck do
    url "https://github.com/fetchcord/FetchCord/releases"
    strategy :github_latest
  end
end
