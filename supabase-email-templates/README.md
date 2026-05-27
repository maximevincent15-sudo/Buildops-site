# Templates emails Supabase — Firovia

Templates HTML en français pour les emails transactionnels envoyés par Supabase Auth.

## Comment les installer dans Supabase

1. Va sur https://supabase.com/dashboard
2. Sélectionne ton projet Firovia
3. Dans le menu de gauche : **Authentication → Emails**
4. Tu verras une liste de templates : `Confirm signup`, `Reset Password`, `Invite user`, etc.
5. Pour chaque template :
   - Clique dessus
   - Remplace le **Subject** et le **Message Body** par les valeurs ci-dessous
   - Clique **Save**

---

## 1. Confirm signup

**Subject :**
```
Confirmez votre inscription sur Firovia
```

**Message Body :** Copie-colle le contenu de `01-confirm-signup.html`

---

## 2. Reset Password

**Subject :**
```
Réinitialisation de votre mot de passe Firovia
```

**Message Body :** Copie-colle le contenu de `02-reset-password.html`

---

## 3. Invite user

**Subject :**
```
Vous êtes invité à rejoindre une équipe sur Firovia
```

**Message Body :** Copie-colle le contenu de `03-invite-user.html`

---

## Variables Supabase utilisées

Ces variables sont automatiquement remplacées par Supabase au moment de l'envoi :

- `{{ .ConfirmationURL }}` — le lien d'action (confirmation, reset, invitation)
- `{{ .Email }}` — l'email du destinataire
- `{{ .SiteURL }}` — l'URL du site (configurée dans Supabase)

---

## Limite actuelle

Tant qu'on n'a pas configuré un SMTP custom (Resend), les emails partent de `noreply@mail.app.supabase.io` — pas de @firovia.fr. C'est la prochaine étape.
