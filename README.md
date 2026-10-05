# World Space Week 2026 · Code Beyond the Earth

Interactive tools and notebooks for [World Space Week 2026](https://www.worldspaceweek.org/) (4–10 October, theme: *Rocket Revolution*), published alongside posts on [Code Beyond the Earth](https://codebeyondtheearth.substack.com).

## Sentinel Overhead

**Live:** `https://<username>.github.io/world-space-week/sentinel-overhead/`

In 1957, the pitch of Sputnik's beep rose as it approached and fell as it moved away, and that Doppler shift was enough to work out its orbit. *Sentinel Overhead* applies the same physics to today's Earth observation satellites:

- lists Sentinel-2 and Sentinel-3 passes over any location for the next five days
- shows each pass as a sky track, a Doppler curve (20 MHz like Sputnik, or an 8.1 GHz X-band downlink) and a pass diagram with the radial velocity and wavefronts
- plays the pass as a Sputnik-style beep compressed to 20 seconds
- available in Turkish, English, German and French

Orbits are propagated with SGP4 in the browser ([satellite.js](https://github.com/shashwatak/satellite-js)). There is no backend.

### Orbital data

A GitHub Actions workflow (`.github/workflows/update-tle.yml`) fetches Sentinel TLEs from [CelesTrak](https://celestrak.org) once a day and commits them to `sentinel-overhead/tle.json`. The page reads that file, so CelesTrak receives one request per day instead of one per visitor. If the file is missing, the page tries CelesTrak directly, and as a last resort falls back to clearly labelled demo orbits.

## Notebooks

| Notebook | What it covers |
|---|---|
| [`sputnik_to_sentinel_doppler.ipynb`](notebooks/sputnik_to_sentinel_doppler.ipynb) | Doppler shift and range-rate derivations, Sentinel passes with Skyfield, the inverse problem (recovering pass geometry from a noisy Doppler curve with `curve_fit`), and a sonified Sputnik pass |

```bash
pip install skyfield sgp4 scipy matplotlib pandas
```

## Further reading

- W. H. Guier & G. C. Weiffenbach, "Genesis of Satellite Navigation", *Johns Hopkins APL Technical Digest* 19(1), 1998
- H. D. Curtis, *Orbital Mechanics for Engineering Students*
- D. A. Vallado, *Fundamentals of Astrodynamics and Applications*
