# assets

Large files for [personal-infra](https://github.com/AnissL93/personal-infra), kept out of the config repos.

- `wallpapers/`: the wallpapers of the desktop colour themes (`NAME-2560.png`, `NAME-3440.png`).
  Theme files in `dotfiles/themes/*.conf` name them; the `theme` script downloads each one into
  `~/.local/share/wallpapers` the first time that theme is used.
- `fonts/`: every font the desktop uses, with licences, originals and previews: [`fonts/README.md`](fonts/README.md).
- `wallpapers/originals/`: the source pictures the theme wallpapers were made from (`NAME-original.*`).

A clone is only needed to add wallpapers (`~/System/assets`); using the themes needs no clone.

## Other wallpaper collections

Not used by any theme; forks kept for browsing, never cloned by the setup:

- [AnissL93/wallpapers](https://github.com/AnissL93/wallpapers) (fork of makccr/wallpapers, ~2.7 GB, mostly 4K)
- [AnissL93/walls-catppuccin-mocha](https://github.com/AnissL93/walls-catppuccin-mocha) (fork of orangci/walls-catppuccin-mocha)

`changebg DIR` sets a random image from any folder, e.g. a clone of one of these.
