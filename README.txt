READ WITH CINDERELLA
====================
A learn-to-read app for the iPad, built with Claude (project: "spelling app").
It started from Spell with Pip and has its own save, so the two apps never mix.

WHAT'S IN THIS FOLDER
  docs/     The finished app. GitHub Pages publishes this folder at
            https://jordantong.github.io/read-with-cinderella/ (repo
            Settings > Pages > Deploy from a branch: main, folder /docs).
            Install it on the iPad from Safari with Share > Add to Home Screen.
  source/   What the app is built from:
              read-with-cinderella.html  the whole app
              build.py                   rebuilds docs/ from the source
              fonts/, icons/             bundled so the app works offline

THE READING PART
  Four question types, all answered by tapping:
    First Sound      hear a sound, tap the picture that starts with it
    Find the Letter  hear a sound and tap its letter, or see a letter and
                     tap the picture that starts with it
    Unicorn Blend    hear c... a... t (your recordings) and tap the picture
    Sound Slide      read a word by tapping or sliding under its letters,
                     then tap the picture
  Reading levels follow the usual phonics order: s a t p i n, then
  m d g o c k, then e u r h b f l, then j v w x y z, then blends (frog,
  tent), then sh ch th ck. She moves up on her own when most words in her
  level are "ready" (3 first-try corrects in a row). Grown-ups can change
  the level and switch question types on or off in Settings.

UPDATING
  Claude edits source/read-with-cinderella.html and reruns build.py, which
  refreshes docs/. Then upload the new docs/ folder to GitHub
  (Add file > Upload files). About a minute later the site updates, and
  the iPad picks up the new version on its next launch or two.

Don't edit files inside docs/ by hand. They are overwritten on every build.
