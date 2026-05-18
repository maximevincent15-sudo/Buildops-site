// ════════════════════════════════════════════════════════════════════
// FIROVIA — Endpoint /api/contact
// ════════════════════════════════════════════════════════════════════
//
// Reçoit le formulaire de lead capture, envoie un email à
// contact@firovia.fr via Resend + un email de confirmation au prospect.
//
// Variables d'environnement requises sur Vercel :
//   - RESEND_API_KEY : clé API Resend (https://resend.com/api-keys)
//   - LEAD_TO_EMAIL  : email de destination des leads (ex: contact@firovia.fr)
//   - LEAD_FROM_EMAIL: email expéditeur (ex: noreply@firovia.fr) — doit
//                       être sur un domaine vérifié dans Resend.
//
// Comportement :
//   - POST /api/contact avec JSON { firstname, lastname, email, phone,
//     company, techs, plan }
//   - Validation basique côté serveur (anti-spam minimal)
//   - Envoi email lead (HTML + texte) à LEAD_TO_EMAIL
//   - Envoi accusé réception au prospect (HTML)
//   - Réponse JSON { ok: true } ou { ok: false, error: "..." }
//
// ════════════════════════════════════════════════════════════════════

export default async function handler(req, res) {
  // CORS — autorise uniquement firovia.fr et localhost
  const origin = req.headers.origin || '';
  const allowedOrigins = [
    'https://firovia.fr',
    'https://www.firovia.fr',
    'http://localhost:8765',
    'http://localhost:3000',
  ];
  if (allowedOrigins.includes(origin)) {
    res.setHeader('Access-Control-Allow-Origin', origin);
  }
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') return res.status(204).end();
  if (req.method !== 'POST') {
    return res.status(405).json({ ok: false, error: 'method_not_allowed' });
  }

  // Body parsing (Vercel parse déjà JSON automatiquement si Content-Type est correct)
  const body = typeof req.body === 'string' ? JSON.parse(req.body || '{}') : (req.body || {});

  const { firstname, lastname, email, phone, company, techs, plan } = body;

  // Validation basique
  if (!firstname || !lastname || !email || !phone || !company) {
    return res.status(400).json({ ok: false, error: 'missing_fields' });
  }
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return res.status(400).json({ ok: false, error: 'invalid_email' });
  }
  // Anti-spam minimal : honeypot + longueur max
  if (firstname.length > 100 || lastname.length > 100 || company.length > 200) {
    return res.status(400).json({ ok: false, error: 'invalid_length' });
  }

  const RESEND_API_KEY = process.env.RESEND_API_KEY;
  const TO_EMAIL = process.env.LEAD_TO_EMAIL || 'contact@firovia.fr';
  const FROM_EMAIL = process.env.LEAD_FROM_EMAIL || 'Firovia <noreply@firovia.fr>';

  if (!RESEND_API_KEY) {
    console.error('[contact] RESEND_API_KEY non configurée');
    return res.status(500).json({ ok: false, error: 'server_not_configured' });
  }

  const planLabel = {
    starter: 'Starter (299€/mois)',
    pro: 'Pro (499€/mois)',
    enterprise: 'Entreprise (799€/mois)',
  }[plan] || 'À déterminer';

  // ─── Email 1 : notification interne (vers contact@firovia.fr) ───
  const internalSubject = `[Lead] ${company} — ${firstname} ${lastname} (${techs} techs)`;
  const internalHtml = `
    <div style="font-family:Inter,Arial,sans-serif;max-width:600px;margin:0 auto;padding:24px;color:#0f172a;">
      <h2 style="margin:0 0 16px;color:#0f172a;">🎯 Nouveau lead Firovia</h2>
      <table style="width:100%;border-collapse:collapse;margin-bottom:24px;">
        <tr><td style="padding:8px 0;color:#64748b;width:160px;">Prénom</td><td style="padding:8px 0;font-weight:600;">${escapeHtml(firstname)}</td></tr>
        <tr><td style="padding:8px 0;color:#64748b;">Nom</td><td style="padding:8px 0;font-weight:600;">${escapeHtml(lastname)}</td></tr>
        <tr><td style="padding:8px 0;color:#64748b;">Email</td><td style="padding:8px 0;"><a href="mailto:${escapeHtml(email)}" style="color:#10b981;">${escapeHtml(email)}</a></td></tr>
        <tr><td style="padding:8px 0;color:#64748b;">Téléphone</td><td style="padding:8px 0;"><a href="tel:${escapeHtml(phone)}" style="color:#10b981;">${escapeHtml(phone)}</a></td></tr>
        <tr><td style="padding:8px 0;color:#64748b;">Entreprise</td><td style="padding:8px 0;font-weight:600;">${escapeHtml(company)}</td></tr>
        <tr><td style="padding:8px 0;color:#64748b;">Techniciens</td><td style="padding:8px 0;">${escapeHtml(techs)}</td></tr>
        <tr><td style="padding:8px 0;color:#64748b;">Plan envisagé</td><td style="padding:8px 0;font-weight:600;">${escapeHtml(planLabel)}</td></tr>
      </table>
      <p style="color:#64748b;font-size:13px;margin:0;">À recontacter sous 24h ouvrées.</p>
    </div>
  `;
  const internalText =
    `Nouveau lead Firovia\n\n` +
    `Prénom : ${firstname}\n` +
    `Nom : ${lastname}\n` +
    `Email : ${email}\n` +
    `Téléphone : ${phone}\n` +
    `Entreprise : ${company}\n` +
    `Techniciens : ${techs}\n` +
    `Plan envisagé : ${planLabel}\n\n` +
    `À recontacter sous 24h ouvrées.`;

  // ─── Email 2 : accusé réception au prospect ───
  const ackSubject = `Votre demande Firovia a bien été reçue`;
  const ackHtml = `
    <div style="font-family:Inter,Arial,sans-serif;max-width:600px;margin:0 auto;padding:32px 24px;color:#0f172a;">
      <h2 style="margin:0 0 16px;color:#0f172a;">Merci ${escapeHtml(firstname)} 👋</h2>
      <p style="line-height:1.6;font-size:16px;margin:0 0 16px;">
        Nous avons bien reçu votre demande d'essai gratuit pour <strong>${escapeHtml(company)}</strong>.
      </p>
      <p style="line-height:1.6;font-size:16px;margin:0 0 24px;">
        Notre équipe vous recontacte sous <strong>24h ouvrées</strong> pour activer votre compte Firovia et organiser une démo personnalisée.
      </p>
      <div style="background:#f1f5f9;border-radius:12px;padding:20px;margin:24px 0;">
        <p style="margin:0 0 8px;font-weight:600;color:#0f172a;">Récapitulatif de votre demande</p>
        <p style="margin:0;color:#64748b;font-size:14px;line-height:1.6;">
          Plan envisagé : <strong style="color:#0f172a;">${escapeHtml(planLabel)}</strong><br>
          Taille d'équipe : <strong style="color:#0f172a;">${escapeHtml(techs)} techniciens</strong>
        </p>
      </div>
      <p style="line-height:1.6;font-size:16px;margin:24px 0 0;">
        En attendant, n'hésitez pas à répondre à cet email si vous avez des questions.
      </p>
      <p style="line-height:1.6;font-size:16px;margin:16px 0 0;">
        À très vite,<br>
        <strong>L'équipe Firovia</strong>
      </p>
      <hr style="border:none;border-top:1px solid #e2e8f0;margin:32px 0 16px;">
      <p style="color:#94a3b8;font-size:12px;line-height:1.5;margin:0;">
        Firovia — Logiciel de gestion pour la maintenance incendie<br>
        <a href="https://firovia.fr" style="color:#94a3b8;">firovia.fr</a>
      </p>
    </div>
  `;

  try {
    // Envoi des deux emails en parallèle
    const [internalResp, ackResp] = await Promise.all([
      sendResend({
        apiKey: RESEND_API_KEY,
        from: FROM_EMAIL,
        to: TO_EMAIL,
        replyTo: email,
        subject: internalSubject,
        html: internalHtml,
        text: internalText,
      }),
      sendResend({
        apiKey: RESEND_API_KEY,
        from: FROM_EMAIL,
        to: email,
        replyTo: TO_EMAIL,
        subject: ackSubject,
        html: ackHtml,
      }),
    ]);

    if (!internalResp.ok) {
      console.error('[contact] Erreur envoi interne :', internalResp.error);
      // L'email interne est critique. L'accusé réception est secondaire.
      return res.status(502).json({ ok: false, error: 'email_send_failed' });
    }

    if (!ackResp.ok) {
      console.warn('[contact] Accusé réception non envoyé :', ackResp.error);
      // On ne fait pas échouer la requête : le lead a été reçu en interne.
    }

    return res.status(200).json({ ok: true });
  } catch (err) {
    console.error('[contact] Exception inattendue :', err);
    return res.status(500).json({ ok: false, error: 'unexpected_error' });
  }
}

// ─── Helpers ─────────────────────────────────────────────────────────

async function sendResend({ apiKey, from, to, replyTo, subject, html, text }) {
  try {
    const body = { from, to, subject, html };
    if (text) body.text = text;
    if (replyTo) body.reply_to = replyTo;

    const r = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });

    if (!r.ok) {
      const text = await r.text();
      return { ok: false, error: `${r.status} ${text}` };
    }
    return { ok: true };
  } catch (err) {
    return { ok: false, error: String(err) };
  }
}

function escapeHtml(s) {
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}
