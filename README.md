# Kit Resto Direct

Site de Kit Resto Direct, un service d'ABD Web Studio : un calculateur gratuit, des guides et la page de vente d'un kit numérique pour aider les restaurants indépendants à faire commander leurs clients en direct, sans commission.

## Structure

- `src/pages/` : le contenu des pages (en-tête entre `---`, puis le HTML).
- `src/layout.html` : la mise en page commune.
- `src/assets/` : styles, calculateur, icône.
- `config.json` : les réglages (adresse du site, lien de paiement, e-mail, informations légales, codes de vérification Google Search Console et Bing, clé IndexNow).
- `build.py` : génère le site dans `site/`.
- `site/` : le site généré, publié tel quel par Cloudflare Pages.

## Modifier le site

```
python3 build.py           # régénère site/ et signale les réglages manquants
python3 build.py --strict  # refuse de générer s'il manque un réglage obligatoire
```

Après chaque modification de `src/` ou de `config.json`, relancez `build.py` et committez aussi `site/`.

## Mise en ligne sur Cloudflare Pages

Projet relié à ce dépôt, sans commande de build, dossier de sortie : `site`.

Le kit payant n'est pas dans ce dépôt public : il est livré par Lemon Squeezy après paiement.
