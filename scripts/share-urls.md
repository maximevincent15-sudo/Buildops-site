# 📊 URLs prêtes à partager (avec UTM tracking)

Copie-colle ces URLs quand tu postes sur les réseaux sociaux, dans tes emails, ou sur des annonces. Tu verras ensuite dans **Vercel Analytics** d'où viennent tes visiteurs.

> ⚠️ Vercel Analytics se trouve dans : Vercel Dashboard → projet **Buildops-site** → onglet **Analytics**.

---

## 🔗 LinkedIn

### Post organique
```
https://firovia.fr/?utm_source=linkedin&utm_medium=social&utm_campaign=organic
```

### Post sponsorisé
```
https://firovia.fr/?utm_source=linkedin&utm_medium=cpc&utm_campaign=2026-launch
```

### Bio LinkedIn (lien profil)
```
https://firovia.fr/?utm_source=linkedin&utm_medium=bio
```

---

## 🐦 X (Twitter)

```
https://firovia.fr/?utm_source=twitter&utm_medium=social
```

---

## 💬 WhatsApp / iMessage (envoi personnel à prospects)

```
https://firovia.fr/?utm_source=whatsapp&utm_medium=dm
```

---

## 📧 Email signature

```
https://firovia.fr/?utm_source=email&utm_medium=signature
```

---

## 📧 Email de prospection (cold)

```
https://firovia.fr/?utm_source=email&utm_medium=cold&utm_campaign=2026-{nom_du_segment}
```

Remplace `{nom_du_segment}` par exemple par `idf-installateurs-extincteurs` ou `lyon-mainteneurs-ssi`.

---

## 📰 Annuaires pros (Sygefor, Pages Jaunes Pro, etc.)

```
https://firovia.fr/?utm_source=annuaire&utm_medium=referral&utm_campaign={nom_annuaire}
```

---

## 🎯 Comment lire les UTM dans Vercel Analytics

1. Va sur **vercel.com/dashboard** → **Buildops-site** → onglet **Analytics**
2. En haut : tu vois les **visiteurs**, **pages vues**, **sources** (où ils viennent)
3. Filtre par **source** ou **medium** pour voir précisément ce qui marche
4. Les UTM apparaissent dans la section **Top Pages** avec leurs query strings

---

## 📐 Convention UTM (pour rester cohérent dans le temps)

| Paramètre | Sens | Exemples |
|---|---|---|
| `utm_source` | D'où vient le visiteur | `linkedin`, `twitter`, `email`, `annuaire` |
| `utm_medium` | Type de canal | `social`, `cpc`, `email`, `bio`, `referral` |
| `utm_campaign` | Nom de la campagne | `2026-launch`, `prospect-idf`, `salon-cnpp` |

**Règle d'or** : toujours en minuscules, pas d'espaces (utilise des `-`), pas d'accents.
