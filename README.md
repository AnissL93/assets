# assets

Large files for [personal-infra](https://github.com/AnissL93/personal-infra), kept out of the config repos.

- `wallpapers/`: the wallpapers of the desktop colour themes (`NAME-2560.png`, `NAME-3440.png`).
  Theme files in `dotfiles/themes/*.conf` name them; the `theme` script downloads each one into
  `~/.local/share/wallpapers` the first time that theme is used.
- `wallpapers/originals/`: the source pictures the theme wallpapers were made from (`NAME-original.*`).

A clone is only needed to add wallpapers (`~/System/assets`); using the themes needs no clone.
