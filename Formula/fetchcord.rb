# typed: strict
# frozen_string_literal: true

# Homebrew formula for FetchCord.
#
# Recommended until the v3.0.0 tag exists:
#
#   brew install --HEAD fetchcord/fetchcord/fetchcord
#
# After the 3.0.0 release (url/sha256 filled by the tap updater):
#
#   brew tap fetchcord/fetchcord
#   brew install fetchcord
#
# To test locally from this repo:
#
#   brew install --HEAD --build-from-source ./Formula/fetchcord.rb

class Fetchcord < Formula
  include Language::Python::Virtualenv

  desc "Display system information as Discord Rich Presence"
  homepage "https://github.com/fetchcord/FetchCord"
  url "https://github.com/fetchcord/FetchCord/archive/refs/tags/v3.0.0.tar.gz"
  sha256 "0000000000000000000000000000000000000000000000000000000000000000"
  license "MIT"
  head "https://github.com/fetchcord/FetchCord.git", branch: "testing"

  depends_on "python@3.12"
  depends_on "fastfetch"

  resource "pypresence" do
    url "https://files.pythonhosted.org/packages/22/ce/4ce38b7f36f4eec77b3d21a5885228bbe8ea6d5ea35ff0876f7889c3bbbd/pypresence-4.6.2.tar.gz"
    sha256 "7e7e93de0e94a42314300ef6d15dd2c44c64ef74b7c749243bc226be2ab90687"
  end

  resource "psutil" do
    url "https://files.pythonhosted.org/packages/aa/c6/d1ddf4abb55e93cebc4f2ed8b5d6dbad109ecb8d63748dd2b20ab5e57ebe/psutil-7.2.2.tar.gz"
    sha256 "0746f5f8d406af344fd547f1c8daa5f5c33dbc293bb8d6a16d80b4bb88f59372"
  end

  resource "pyyaml" do
    url "https://files.pythonhosted.org/packages/05/8e/961c0007c59b8dd7729d542c61a4d537767a59645b82a0b521206e1e25c2/pyyaml-6.0.3.tar.gz"
    sha256 "d76623373421df22fb4cf8817020cbb7ef15c725b9d5e45f17e189bfc384190f"
  end

  def install
    virtualenv_install_with_resources
  end

  test do
    assert_match "FetchCord version:", shell_output("#{bin}/fetchcord --version")
  end

  livecheck do
    url "https://github.com/fetchcord/FetchCord/releases"
    strategy :github_latest
  end
end
