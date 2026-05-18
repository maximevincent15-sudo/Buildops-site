-- ════════════════════════════════════════════════════════════════════
-- FIROVIA — Script d'anonymisation des données de démonstration
-- ════════════════════════════════════════════════════════════════════
--
-- Objectif : remplacer les noms réels (clients, organisation, profil,
-- techniciens) par des données fictives crédibles pour les screenshots
-- du site vitrine.
--
-- À LANCER UNE SEULE FOIS dans Supabase SQL Editor.
--
-- ⚠️ Les données sont MODIFIÉES (pas de revert auto).
--    Si tu veux revenir en arrière, il faudra le faire manuellement.
--
-- ════════════════════════════════════════════════════════════════════

-- ─── 1. RENOMMER L'ORGANISATION ─────────────────────────────────────
update public.organizations
   set name = 'Firovia Démo'
 where name ilike '%sécurité pro test%'
    or name ilike '%securite pro test%'
    or name ilike '%test%';


-- ─── 2. RENOMMER LE PROFIL ADMIN ────────────────────────────────────
update public.profiles
   set first_name = 'Marc',
       last_name  = 'Dupont'
 where first_name ilike '%maxime%' or last_name ilike '%vincent%';


-- ─── 3. RENOMMER LES TECHNICIENS ────────────────────────────────────
-- Thomas Moreau (commercial → technicien sénior)
update public.technicians
   set first_name = 'Thomas',
       last_name  = 'Moreau',
       email      = 'thomas.moreau@firovia-demo.fr',
       phone      = '06 12 34 56 78',
       role       = 'Technicien sénior'
 where first_name ilike '%thomas%' and last_name ilike '%moreau%';

-- Julien Pariseau (fix typo "techncien" → "Technicien")
update public.technicians
   set first_name = 'Julien',
       last_name  = 'Pariseau',
       email      = 'julien.pariseau@firovia-demo.fr',
       phone      = '06 23 45 67 89',
       role       = 'Technicien'
 where first_name ilike '%julien%' and last_name ilike '%pariseau%';


-- ─── 4. RENOMMER LES CLIENTS ────────────────────────────────────────
-- Antoine Crome → Crozet BTP & Fils (PARIS)
update public.clients
   set name          = 'Crozet BTP & Fils',
       contact_name  = 'M. Crozet',
       contact_email = 'contact@crozet-btp.fr',
       contact_phone = '01 42 56 78 90',
       address       = '24 Avenue de la République, 75011 Paris'
 where name ilike '%antoine crome%';

-- Bernard Vincent Entreprises → Vincent & Associés (LYON)
update public.clients
   set name          = 'Vincent & Associés',
       contact_name  = 'M. Vincent',
       contact_email = 'contact@vincent-associes.fr',
       contact_phone = '04 72 34 56 78',
       address       = '15 Rue de la République, 69002 Lyon'
 where name ilike '%bernard vincent%';

-- Résidence Le Marly → Résidence Les Tilleuls (RENNES, nouvelle adresse fictive)
update public.clients
   set name          = 'Résidence Les Tilleuls',
       contact_name  = 'Syndic Les Tilleuls',
       contact_email = 'syndic@les-tilleuls.fr',
       contact_phone = '02 99 12 34 56',
       address       = '24 Boulevard de la Liberté, 35000 Rennes'
 where name ilike '%marly%' or name ilike '%tilleuls%';

-- Soprema → Toiture Pro Nord (LILLE)
-- (Anonymisation supplémentaire : Romain Levacher → Marc Lambert)
update public.clients
   set name          = 'Toiture Pro Nord',
       contact_name  = 'Marc Lambert',
       contact_email = 'contact@toiture-pro-nord.fr',
       contact_phone = '03 20 45 67 89',
       address       = '42 Rue Faidherbe, 59000 Lille'
 where name ilike '%soprema%' or contact_name ilike '%levacher%';

-- Hopital Le Chesnay → Clinique du Parc (MARSEILLE)
update public.clients
   set name          = 'Clinique du Parc',
       contact_name  = 'Direction technique',
       contact_email = 'technique@clinique-du-parc.fr',
       contact_phone = '04 91 23 45 67',
       address       = '12 Avenue du Prado, 13008 Marseille'
 where name ilike '%hopital%' or name ilike '%hôpital%' or name ilike '%hoptial%';

-- Valoris SA → Tertiaire Services (BORDEAUX)
update public.clients
   set name          = 'Tertiaire Services',
       contact_name  = 'Service maintenance',
       contact_email = 'maintenance@tertiaire-services.fr',
       contact_phone = '05 56 78 90 12',
       address       = '7 Cours de l''Intendance, 33000 Bordeaux'
 where name ilike '%valoris%';

-- test firovia → Démo Firovia (PARIS)
update public.clients
   set name          = 'Démo Firovia',
       contact_name  = 'Service démo',
       contact_email = 'demo@firovia-demo.fr',
       contact_phone = '01 23 45 67 89',
       address       = '5 Place de la Concorde, 75008 Paris'
 where name ilike '%test firovia%' or name ilike '%firovia%';

-- julien csb → Levavasseur SARL (TOULOUSE)
update public.clients
   set name          = 'Levavasseur SARL',
       contact_name  = 'Mme Levavasseur',
       contact_email = 'contact@levavasseur.fr',
       contact_phone = '05 61 34 56 78',
       address       = '18 Place du Capitole, 31000 Toulouse'
 where name ilike '%julien csb%';


-- ─── 5. PROPAGER LES NOUVEAUX NOMS DANS LES INTERVENTIONS ──────────
-- (le champ client_name est un snapshot, il faut le mettre à jour)

update public.interventions set client_name = 'Crozet BTP & Fils'         where client_name ilike '%antoine crome%';
update public.interventions set client_name = 'Vincent & Associés'        where client_name ilike '%bernard vincent%';
update public.interventions set client_name = 'Résidence Les Tilleuls'    where client_name ilike '%marly%';
update public.interventions set client_name = 'Toiture Pro 78'            where client_name ilike '%soprema%';
update public.interventions set client_name = 'Clinique du Parc'          where client_name ilike '%hopital%' or client_name ilike '%hôpital%' or client_name ilike '%hoptial%';
update public.interventions set client_name = 'Tertiaire Services'        where client_name ilike '%valoris%';
update public.interventions set client_name = 'Démo Firovia'              where client_name ilike '%test firovia%';
update public.interventions set client_name = 'Levavasseur SARL'          where client_name ilike '%julien csb%';
update public.interventions set client_name = 'Démo Test Urgence'         where client_name ilike '%test urgence%';
update public.interventions set client_name = 'Démo Test Client'          where client_name ilike '%test client%';

-- Sites (rename pour grandes villes)
update public.interventions set site_name = 'Mairie de Paris 11e'         where site_name ilike '%mairie de paris%';
update public.interventions set site_name = 'Bâtiment A'                   where site_name ilike '%batiment%' or site_name = 'Bâtiment A';
update public.interventions set site_name = 'École primaire Jean Jaurès'  where site_name ilike '%ecole%' or site_name ilike '%école%';
update public.interventions set site_name = 'Clinique — bâtiment principal' where site_name ilike '%hopital%' or site_name ilike '%hôpital%' or site_name ilike '%hoptial%';
update public.interventions set site_name = 'Mairie de Lyon 2e'           where site_name = 'mairie' or site_name = 'Mairie';
update public.interventions set site_name = 'Mairie de Lyon 2e'           where site_name ilike '%mairie%' and not site_name ilike '%lyon%' and not site_name ilike '%paris%' and not site_name ilike '%rennes%';

-- Technicien names (snapshot)
update public.interventions set technician_name = 'Thomas Moreau'         where technician_name ilike '%thomas%';
update public.interventions set technician_name = 'Julien Pariseau'       where technician_name ilike '%julien%' and technician_name not ilike '%csb%';
update public.interventions set technician_name = 'Marc Dupont'           where technician_name ilike '%maxime%';
update public.interventions set technician_name = 'Nathan Bernard'        where technician_name ilike '%nathan%';
update public.interventions set technician_name = 'Paul Garnier'          where technician_name ilike '%paul%';
update public.interventions set technician_name = 'Enzo Lemoine'          where technician_name ilike '%enzo%';


-- ─── 6. PROPAGER DANS LES DEVIS (quotes) ────────────────────────────
update public.quotes set client_name = 'Crozet BTP & Fils',          client_email = 'contact@crozet-btp.fr',          client_address = '12 Rue des Lilas, 78000 Versailles'     where client_name ilike '%antoine crome%';
update public.quotes set client_name = 'Vincent & Associés',         client_email = 'contact@vincent-associes.fr',     client_address = '8 Avenue Foch, 92000 Boulogne'         where client_name ilike '%bernard vincent%';
update public.quotes set client_name = 'Résidence Les Tilleuls',     client_email = 'syndic@les-tilleuls.fr',          client_address = '15 Allée des Tilleuls, 78290 Croissy'  where client_name ilike '%marly%';
update public.quotes set client_name = 'Démo Firovia',               client_email = 'demo@firovia-demo.fr',            client_address = '1 Rue de la Démo, 75001 Paris'         where client_name ilike '%test firovia%';


-- ─── 7. PROPAGER DANS LES FACTURES (invoices) ───────────────────────
update public.invoices set client_name = 'Crozet BTP & Fils',         client_email = 'contact@crozet-btp.fr',          client_address = '12 Rue des Lilas, 78000 Versailles'    where client_name ilike '%antoine crome%';
update public.invoices set client_name = 'Vincent & Associés',        client_email = 'contact@vincent-associes.fr',    client_address = '8 Avenue Foch, 92000 Boulogne'         where client_name ilike '%bernard vincent%';
update public.invoices set client_name = 'Résidence Les Tilleuls',    client_email = 'syndic@les-tilleuls.fr',          client_address = '15 Allée des Tilleuls, 78290 Croissy'  where client_name ilike '%marly%';


-- ─── 8. RAPPORTS (si client_name présent dans la table) ───────────
-- Note : reports n'a peut-être pas de client_name direct (vient via intervention)
-- Pas d'update nécessaire dans la plupart des cas.


-- ─── 9. ANONYMISATION ÉMAIL PERSO (toutes tables) ──────────────────
-- Remplace tout emploi de l'email perso maximevincent15@gmail.com
-- par un email fictif générique pour la démo.

update public.clients
   set contact_email = 'marc.dupont@firovia-demo.fr'
 where contact_email ilike '%maximevincent15%' or contact_email ilike '%@gmail.com';

update public.quotes
   set client_email = 'marc.dupont@firovia-demo.fr'
 where client_email ilike '%maximevincent15%' or client_email ilike '%@gmail.com';

update public.invoices
   set client_email = 'marc.dupont@firovia-demo.fr'
 where client_email ilike '%maximevincent15%' or client_email ilike '%@gmail.com';

-- Si email perso présent dans profiles (membres de l'organisation de démo)
update public.profiles
   set first_name = 'Démo',
       last_name  = 'Compte'
 where id in (
   select id from auth.users where email ilike '%maximevincent15%'
 );


-- ═══════════════════════════════════════════════════════════════════
-- ✅ Anonymisation terminée. Tu peux re-capturer tes screenshots.
-- ═══════════════════════════════════════════════════════════════════
