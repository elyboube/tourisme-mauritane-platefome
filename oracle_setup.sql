-- =====================================================================
-- PLATEFORME TOURISME MAURITANIE - Script Oracle Complet
-- Utilisateur technique : tourisme_user
-- =====================================================================

-- ─── 1. CRÉER L'UTILISATEUR ORACLE TECHNIQUE ────────────────────────
CREATE USER tourisme_user IDENTIFIED BY tourisme_pass123
    DEFAULT TABLESPACE USERS
    TEMPORARY TABLESPACE TEMP
    QUOTA UNLIMITED ON USERS;

-- Rôle dédié
CREATE ROLE role_tourisme;

GRANT CONNECT TO role_tourisme;
GRANT CREATE SESSION TO role_tourisme;
GRANT role_tourisme TO tourisme_user;

-- Privilèges minimaux (principe du moindre privilège)
GRANT SELECT, INSERT, UPDATE, DELETE ON tourisme_user.UTILISATEUR      TO role_tourisme;
GRANT SELECT, INSERT, UPDATE, DELETE ON tourisme_user.DESTINATION       TO role_tourisme;
GRANT SELECT, INSERT, UPDATE, DELETE ON tourisme_user.HEBERGEMENT       TO role_tourisme;
GRANT SELECT, INSERT, UPDATE, DELETE ON tourisme_user.GUIDE             TO role_tourisme;
GRANT SELECT, INSERT, UPDATE, DELETE ON tourisme_user.RESERVATION       TO role_tourisme;
GRANT SELECT, INSERT, UPDATE, DELETE ON tourisme_user.COMMENTAIRE       TO role_tourisme;
GRANT SELECT, INSERT, UPDATE, DELETE ON tourisme_user.FAVORI            TO role_tourisme;
GRANT SELECT, INSERT, UPDATE, DELETE ON tourisme_user.NOTIFICATION      TO role_tourisme;
GRANT EXECUTE ON tourisme_user.PKG_RESERVATION  TO role_tourisme;
GRANT EXECUTE ON tourisme_user.PKG_STATISTIQUES TO role_tourisme;


-- ─── 2. SÉQUENCES ───────────────────────────────────────────────────
CREATE SEQUENCE seq_utilisateur    START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE seq_destination    START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE seq_hebergement    START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE seq_guide          START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE seq_reservation    START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE seq_commentaire    START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE seq_notification   START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE seq_region         START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;


-- ─── 3. TABLES ──────────────────────────────────────────────────────

-- Région
CREATE TABLE REGION (
    id          NUMBER PRIMARY KEY,
    nom         VARCHAR2(100) NOT NULL,
    description CLOB,
    CONSTRAINT uq_region_nom UNIQUE (nom)
);

-- Utilisateur
CREATE TABLE UTILISATEUR (
    id               NUMBER PRIMARY KEY,
    username         VARCHAR2(150) NOT NULL,
    password         VARCHAR2(256) NOT NULL,
    email            VARCHAR2(254) NOT NULL,
    first_name       VARCHAR2(150),
    last_name        VARCHAR2(150),
    role             VARCHAR2(20) DEFAULT 'visiteur' NOT NULL,
    telephone        VARCHAR2(20),
    adresse          VARCHAR2(255),
    pays             VARCHAR2(100),
    photo_profil     VARCHAR2(300),
    date_inscription TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
    est_actif        NUMBER(1)  DEFAULT 1 NOT NULL,
    is_superuser     NUMBER(1)  DEFAULT 0 NOT NULL,
    is_staff         NUMBER(1)  DEFAULT 0 NOT NULL,
    last_login       TIMESTAMP,
    CONSTRAINT uq_utilisateur_username UNIQUE (username),
    CONSTRAINT uq_utilisateur_email    UNIQUE (email),
    CONSTRAINT chk_role CHECK (role IN ('visiteur','utilisateur','admin')),
    CONSTRAINT chk_est_actif CHECK (est_actif IN (0,1))
);

-- Destination
CREATE TABLE DESTINATION (
    id               NUMBER PRIMARY KEY,
    nom              VARCHAR2(200) NOT NULL,
    description      CLOB         NOT NULL,
    region_id        NUMBER       REFERENCES REGION(id) ON DELETE SET NULL,
    latitude         NUMBER(10,7),
    longitude        NUMBER(10,7),
    image_principale VARCHAR2(300),
    video_url        VARCHAR2(500),
    prix_entree      NUMBER(10,2) DEFAULT 0 NOT NULL,
    est_active       NUMBER(1)    DEFAULT 1 NOT NULL,
    date_creation    TIMESTAMP    DEFAULT SYSTIMESTAMP NOT NULL,
    note_moyenne     NUMBER(3,2)  DEFAULT 0 NOT NULL,
    nb_commentaires  NUMBER       DEFAULT 0 NOT NULL,
    CONSTRAINT chk_dest_active    CHECK (est_active IN (0,1)),
    CONSTRAINT chk_prix_entree    CHECK (prix_entree >= 0),
    CONSTRAINT chk_note_dest      CHECK (note_moyenne BETWEEN 0 AND 5)
);

-- Type Hébergement
CREATE TABLE TYPE_HEBERGEMENT (
    id    NUMBER PRIMARY KEY,
    nom   VARCHAR2(100) NOT NULL,
    icone VARCHAR2(50)  DEFAULT 'fa-hotel',
    CONSTRAINT uq_type_heberg_nom UNIQUE (nom)
);

-- Hébergement
CREATE TABLE HEBERGEMENT (
    id                  NUMBER PRIMARY KEY,
    nom                 VARCHAR2(200)  NOT NULL,
    type_hebergement_id NUMBER         REFERENCES TYPE_HEBERGEMENT(id) ON DELETE SET NULL,
    destination_id      NUMBER         NOT NULL REFERENCES DESTINATION(id) ON DELETE CASCADE,
    description         CLOB           NOT NULL,
    adresse             VARCHAR2(300)  NOT NULL,
    latitude            NUMBER(10,7),
    longitude           NUMBER(10,7),
    telephone           VARCHAR2(20),
    email               VARCHAR2(254),
    site_web            VARCHAR2(500),
    image_principale    VARCHAR2(300),
    prix_nuit           NUMBER(10,2)   NOT NULL,
    capacite            NUMBER         DEFAULT 1 NOT NULL,
    nb_chambres         NUMBER         DEFAULT 1 NOT NULL,
    est_actif           NUMBER(1)      DEFAULT 1 NOT NULL,
    est_verifie         NUMBER(1)      DEFAULT 0 NOT NULL,
    wifi                NUMBER(1)      DEFAULT 0,
    piscine             NUMBER(1)      DEFAULT 0,
    climatisation       NUMBER(1)      DEFAULT 0,
    parking             NUMBER(1)      DEFAULT 0,
    restaurant          NUMBER(1)      DEFAULT 0,
    date_creation       TIMESTAMP      DEFAULT SYSTIMESTAMP NOT NULL,
    note_moyenne        NUMBER(3,2)    DEFAULT 0 NOT NULL,
    CONSTRAINT chk_prix_nuit  CHECK (prix_nuit > 0),
    CONSTRAINT chk_capacite   CHECK (capacite >= 1),
    CONSTRAINT chk_note_heb   CHECK (note_moyenne BETWEEN 0 AND 5)
);

-- Guide
CREATE TABLE GUIDE (
    id            NUMBER PRIMARY KEY,
    nom           VARCHAR2(200)  NOT NULL,
    prenom        VARCHAR2(200)  NOT NULL,
    email         VARCHAR2(254)  NOT NULL,
    telephone     VARCHAR2(20)   NOT NULL,
    photo         VARCHAR2(300),
    biographie    CLOB           NOT NULL,
    langues       VARCHAR2(200),
    specialites   CLOB,
    prix_journee  NUMBER(10,2)   NOT NULL,
    est_disponible NUMBER(1)     DEFAULT 1 NOT NULL,
    est_verifie    NUMBER(1)     DEFAULT 0 NOT NULL,
    date_creation  TIMESTAMP     DEFAULT SYSTIMESTAMP NOT NULL,
    note_moyenne   NUMBER(3,2)   DEFAULT 0 NOT NULL,
    CONSTRAINT uq_guide_email CHECK (email IS NOT NULL),
    CONSTRAINT chk_prix_journee CHECK (prix_journee > 0),
    CONSTRAINT chk_note_guide   CHECK (note_moyenne BETWEEN 0 AND 5)
);

-- Réservation
CREATE TABLE RESERVATION (
    id               NUMBER PRIMARY KEY,
    utilisateur_id   NUMBER      NOT NULL REFERENCES UTILISATEUR(id) ON DELETE CASCADE,
    destination_id   NUMBER      REFERENCES DESTINATION(id) ON DELETE SET NULL,
    type_reservation VARCHAR2(20) NOT NULL,
    hebergement_id   NUMBER      REFERENCES HEBERGEMENT(id) ON DELETE SET NULL,
    guide_id         NUMBER      REFERENCES GUIDE(id) ON DELETE SET NULL,
    date_debut       DATE        NOT NULL,
    date_fin         DATE        NOT NULL,
    nb_personnes     NUMBER      DEFAULT 1 NOT NULL,
    statut           VARCHAR2(20) DEFAULT 'en_attente' NOT NULL,
    prix_total       NUMBER(12,2) DEFAULT 0 NOT NULL,
    notes            CLOB,
    date_creation    TIMESTAMP   DEFAULT SYSTIMESTAMP NOT NULL,
    date_modification TIMESTAMP  DEFAULT SYSTIMESTAMP NOT NULL,
    confirme_par_id  NUMBER      REFERENCES UTILISATEUR(id) ON DELETE SET NULL,
    CONSTRAINT chk_dates_resa    CHECK (date_fin >= date_debut),
    CONSTRAINT chk_nb_personnes  CHECK (nb_personnes >= 1),
    CONSTRAINT chk_statut_resa   CHECK (statut IN ('en_attente','confirmee','annulee','terminee')),
    CONSTRAINT chk_type_resa     CHECK (type_reservation IN ('hebergement','guide','package'))
);

-- Commentaire
CREATE TABLE COMMENTAIRE (
    id              NUMBER PRIMARY KEY,
    utilisateur_id  NUMBER   NOT NULL REFERENCES UTILISATEUR(id) ON DELETE CASCADE,
    destination_id  NUMBER   REFERENCES DESTINATION(id) ON DELETE CASCADE,
    hebergement_id  NUMBER   REFERENCES HEBERGEMENT(id) ON DELETE CASCADE,
    guide_id        NUMBER   REFERENCES GUIDE(id) ON DELETE CASCADE,
    note            NUMBER   NOT NULL,
    texte           CLOB     NOT NULL,
    date_creation   TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
    est_approuve    NUMBER(1) DEFAULT 1 NOT NULL,
    CONSTRAINT chk_note_valide  CHECK (note BETWEEN 1 AND 5),
    CONSTRAINT chk_cible_unique CHECK (
        (destination_id IS NOT NULL AND hebergement_id IS NULL AND guide_id IS NULL) OR
        (destination_id IS NULL AND hebergement_id IS NOT NULL AND guide_id IS NULL) OR
        (destination_id IS NULL AND hebergement_id IS NULL AND guide_id IS NOT NULL)
    )
);

-- Favori
CREATE TABLE FAVORI (
    id              NUMBER PRIMARY KEY,
    utilisateur_id  NUMBER NOT NULL REFERENCES UTILISATEUR(id) ON DELETE CASCADE,
    destination_id  NUMBER REFERENCES DESTINATION(id) ON DELETE CASCADE,
    hebergement_id  NUMBER REFERENCES HEBERGEMENT(id) ON DELETE CASCADE,
    guide_id        NUMBER REFERENCES GUIDE(id) ON DELETE CASCADE,
    date_ajout      TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL
);

-- Notification
CREATE TABLE NOTIFICATION (
    id             NUMBER PRIMARY KEY,
    utilisateur_id NUMBER      NOT NULL REFERENCES UTILISATEUR(id) ON DELETE CASCADE,
    type_notif     VARCHAR2(20) NOT NULL,
    titre          VARCHAR2(200) NOT NULL,
    message        CLOB         NOT NULL,
    est_lu         NUMBER(1)    DEFAULT 0 NOT NULL,
    date_creation  TIMESTAMP    DEFAULT SYSTIMESTAMP NOT NULL,
    reservation_id NUMBER       REFERENCES RESERVATION(id) ON DELETE CASCADE,
    CONSTRAINT chk_type_notif CHECK (type_notif IN ('reservation','confirmation','annulation','info'))
);

-- Guide_Destination (M2M)
CREATE TABLE GUIDE_DESTINATION (
    guide_id       NUMBER NOT NULL REFERENCES GUIDE(id) ON DELETE CASCADE,
    destination_id NUMBER NOT NULL REFERENCES DESTINATION(id) ON DELETE CASCADE,
    CONSTRAINT pk_guide_dest PRIMARY KEY (guide_id, destination_id)
);


-- ─── 4. INDEX ────────────────────────────────────────────────────────
CREATE INDEX idx_resa_utilisateur  ON RESERVATION(utilisateur_id);
CREATE INDEX idx_resa_statut       ON RESERVATION(statut);
CREATE INDEX idx_resa_dates        ON RESERVATION(date_debut, date_fin);
CREATE INDEX idx_comment_dest      ON COMMENTAIRE(destination_id);
CREATE INDEX idx_comment_heb       ON COMMENTAIRE(hebergement_id);
CREATE INDEX idx_dest_region       ON DESTINATION(region_id);
CREATE INDEX idx_heb_dest          ON HEBERGEMENT(destination_id);


-- ─── 5. TRIGGERS ─────────────────────────────────────────────────────

-- TRIGGER 1 : Auto-incrément ID avec séquence
CREATE OR REPLACE TRIGGER trg_region_bi
    BEFORE INSERT ON REGION FOR EACH ROW
BEGIN
    IF :NEW.id IS NULL THEN
        :NEW.id := seq_region.NEXTVAL;
    END IF;
END;
/

CREATE OR REPLACE TRIGGER trg_utilisateur_bi
    BEFORE INSERT ON UTILISATEUR FOR EACH ROW
BEGIN
    IF :NEW.id IS NULL THEN
        :NEW.id := seq_utilisateur.NEXTVAL;
    END IF;
    :NEW.date_inscription := SYSTIMESTAMP;
END;
/

CREATE OR REPLACE TRIGGER trg_destination_bi
    BEFORE INSERT ON DESTINATION FOR EACH ROW
BEGIN
    IF :NEW.id IS NULL THEN
        :NEW.id := seq_destination.NEXTVAL;
    END IF;
END;
/

CREATE OR REPLACE TRIGGER trg_hebergement_bi
    BEFORE INSERT ON HEBERGEMENT FOR EACH ROW
BEGIN
    IF :NEW.id IS NULL THEN
        :NEW.id := seq_hebergement.NEXTVAL;
    END IF;
END;
/

CREATE OR REPLACE TRIGGER trg_guide_bi
    BEFORE INSERT ON GUIDE FOR EACH ROW
BEGIN
    IF :NEW.id IS NULL THEN
        :NEW.id := seq_guide.NEXTVAL;
    END IF;
END;
/

CREATE OR REPLACE TRIGGER trg_reservation_bi
    BEFORE INSERT ON RESERVATION FOR EACH ROW
BEGIN
    IF :NEW.id IS NULL THEN
        :NEW.id := seq_reservation.NEXTVAL;
    END IF;
    :NEW.date_creation    := SYSTIMESTAMP;
    :NEW.date_modification := SYSTIMESTAMP;
    -- Calcul automatique du prix total
    :NEW.prix_total := PKG_RESERVATION.calculer_prix(
        :NEW.type_reservation,
        :NEW.hebergement_id,
        :NEW.guide_id,
        :NEW.date_debut,
        :NEW.date_fin,
        :NEW.nb_personnes
    );
END;
/

CREATE OR REPLACE TRIGGER trg_reservation_bu
    BEFORE UPDATE ON RESERVATION FOR EACH ROW
BEGIN
    :NEW.date_modification := SYSTIMESTAMP;
    -- Recalcul si les paramètres tarifaires changent
    IF :OLD.hebergement_id != :NEW.hebergement_id OR
       :OLD.guide_id        != :NEW.guide_id OR
       :OLD.date_debut      != :NEW.date_debut OR
       :OLD.date_fin        != :NEW.date_fin OR
       :OLD.nb_personnes    != :NEW.nb_personnes THEN
        :NEW.prix_total := PKG_RESERVATION.calculer_prix(
            :NEW.type_reservation,
            :NEW.hebergement_id,
            :NEW.guide_id,
            :NEW.date_debut,
            :NEW.date_fin,
            :NEW.nb_personnes
        );
    END IF;
END;
/

-- TRIGGER 2 : Notification automatique lors d'une nouvelle réservation
CREATE OR REPLACE TRIGGER trg_notif_nouvelle_reservation
    AFTER INSERT ON RESERVATION FOR EACH ROW
DECLARE
    v_notif_id NUMBER := seq_notification.NEXTVAL;
    v_dest_nom  VARCHAR2(200);
BEGIN
    SELECT nom INTO v_dest_nom FROM DESTINATION WHERE id = :NEW.destination_id;

    INSERT INTO NOTIFICATION (id, utilisateur_id, type_notif, titre, message, reservation_id)
    VALUES (
        v_notif_id,
        :NEW.utilisateur_id,
        'reservation',
        'Réservation créée avec succès',
        'Votre réservation pour ' || v_dest_nom ||
        ' du ' || TO_CHAR(:NEW.date_debut, 'DD/MM/YYYY') ||
        ' au ' || TO_CHAR(:NEW.date_fin, 'DD/MM/YYYY') ||
        ' a été enregistrée. Prix total : ' || :NEW.prix_total || ' MRU.',
        :NEW.id
    );
EXCEPTION
    WHEN NO_DATA_FOUND THEN NULL;
END;
/

-- TRIGGER 3 : Notification lors de confirmation/annulation
CREATE OR REPLACE TRIGGER trg_notif_changement_statut
    AFTER UPDATE OF statut ON RESERVATION FOR EACH ROW
WHEN (OLD.statut != NEW.statut)
DECLARE
    v_notif_id  NUMBER := seq_notification.NEXTVAL;
    v_titre     VARCHAR2(200);
    v_message   CLOB;
    v_type_notif VARCHAR2(20);
BEGIN
    IF :NEW.statut = 'confirmee' THEN
        v_type_notif := 'confirmation';
        v_titre      := 'Réservation confirmée !';
        v_message    := 'Votre réservation #' || :NEW.id || ' a été confirmée par notre équipe. Bon voyage en Mauritanie !';
    ELSIF :NEW.statut = 'annulee' THEN
        v_type_notif := 'annulation';
        v_titre      := 'Réservation annulée';
        v_message    := 'Votre réservation #' || :NEW.id || ' a été annulée.';
    ELSIF :NEW.statut = 'terminee' THEN
        v_type_notif := 'info';
        v_titre      := 'Séjour terminé - Donnez votre avis !';
        v_message    := 'Votre séjour est terminé. Nous espérons que vous avez apprécié votre visite. N''hésitez pas à laisser un commentaire !';
    ELSE
        RETURN;
    END IF;

    INSERT INTO NOTIFICATION (id, utilisateur_id, type_notif, titre, message, reservation_id)
    VALUES (v_notif_id, :NEW.utilisateur_id, v_type_notif, v_titre, v_message, :NEW.id);
END;
/

-- TRIGGER 4 : Mise à jour automatique note_moyenne et nb_commentaires après un commentaire
CREATE OR REPLACE TRIGGER trg_maj_notes_apres_commentaire
    AFTER INSERT OR UPDATE OR DELETE ON COMMENTAIRE FOR EACH ROW
BEGIN
    -- Mise à jour destination
    IF COALESCE(:NEW.destination_id, :OLD.destination_id) IS NOT NULL THEN
        UPDATE DESTINATION
        SET note_moyenne    = (SELECT ROUND(AVG(note), 2) FROM COMMENTAIRE
                               WHERE destination_id = COALESCE(:NEW.destination_id, :OLD.destination_id)
                               AND est_approuve = 1),
            nb_commentaires = (SELECT COUNT(*) FROM COMMENTAIRE
                               WHERE destination_id = COALESCE(:NEW.destination_id, :OLD.destination_id)
                               AND est_approuve = 1)
        WHERE id = COALESCE(:NEW.destination_id, :OLD.destination_id);
    END IF;

    -- Mise à jour hébergement
    IF COALESCE(:NEW.hebergement_id, :OLD.hebergement_id) IS NOT NULL THEN
        UPDATE HEBERGEMENT
        SET note_moyenne = (SELECT ROUND(AVG(note), 2) FROM COMMENTAIRE
                            WHERE hebergement_id = COALESCE(:NEW.hebergement_id, :OLD.hebergement_id)
                            AND est_approuve = 1)
        WHERE id = COALESCE(:NEW.hebergement_id, :OLD.hebergement_id);
    END IF;

    -- Mise à jour guide
    IF COALESCE(:NEW.guide_id, :OLD.guide_id) IS NOT NULL THEN
        UPDATE GUIDE
        SET note_moyenne = (SELECT ROUND(AVG(note), 2) FROM COMMENTAIRE
                            WHERE guide_id = COALESCE(:NEW.guide_id, :OLD.guide_id)
                            AND est_approuve = 1)
        WHERE id = COALESCE(:NEW.guide_id, :OLD.guide_id);
    END IF;
END;
/

-- TRIGGER 5 : Vérification disponibilité avant réservation hébergement (chevauchement)
CREATE OR REPLACE TRIGGER trg_verif_dispo_hebergement
    BEFORE INSERT ON RESERVATION FOR EACH ROW
WHEN (NEW.hebergement_id IS NOT NULL)
DECLARE
    v_nb_reservations NUMBER;
    v_capacite        NUMBER;
    v_reservations_actives NUMBER;
BEGIN
    SELECT capacite INTO v_capacite
    FROM HEBERGEMENT WHERE id = :NEW.hebergement_id;

    SELECT COUNT(*) INTO v_reservations_actives
    FROM RESERVATION
    WHERE hebergement_id = :NEW.hebergement_id
      AND statut NOT IN ('annulee')
      AND date_debut < :NEW.date_fin
      AND date_fin   > :NEW.date_debut;

    IF v_reservations_actives >= v_capacite THEN
        RAISE_APPLICATION_ERROR(-20001,
            'Hébergement complet pour les dates sélectionnées. Veuillez choisir d''autres dates.');
    END IF;
END;
/

-- TRIGGER 6 : Vérification disponibilité guide (pas de double réservation)
CREATE OR REPLACE TRIGGER trg_verif_dispo_guide
    BEFORE INSERT ON RESERVATION FOR EACH ROW
WHEN (NEW.guide_id IS NOT NULL)
DECLARE
    v_conflit NUMBER;
BEGIN
    SELECT COUNT(*) INTO v_conflit
    FROM RESERVATION
    WHERE guide_id = :NEW.guide_id
      AND statut NOT IN ('annulee')
      AND date_debut < :NEW.date_fin
      AND date_fin   > :NEW.date_debut;

    IF v_conflit > 0 THEN
        RAISE_APPLICATION_ERROR(-20002,
            'Ce guide est déjà réservé pour ces dates. Veuillez choisir un autre guide ou d''autres dates.');
    END IF;
END;
/

-- TRIGGER 7 : Interdire de supprimer une réservation confirmée (sécurité)
CREATE OR REPLACE TRIGGER trg_interdire_suppression_resa_confirmee
    BEFORE DELETE ON RESERVATION FOR EACH ROW
WHEN (OLD.statut = 'confirmee')
BEGIN
    RAISE_APPLICATION_ERROR(-20003,
        'Impossible de supprimer une réservation confirmée. Veuillez d''abord l''annuler.');
END;
/

-- TRIGGER 8 : Audit - historique des changements de statut réservation
CREATE TABLE AUDIT_RESERVATION (
    id             NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    reservation_id NUMBER,
    ancien_statut  VARCHAR2(20),
    nouveau_statut VARCHAR2(20),
    modifie_par    NUMBER,
    date_modif     TIMESTAMP DEFAULT SYSTIMESTAMP
);

CREATE OR REPLACE TRIGGER trg_audit_statut_reservation
    AFTER UPDATE OF statut ON RESERVATION FOR EACH ROW
WHEN (OLD.statut != NEW.statut)
BEGIN
    INSERT INTO AUDIT_RESERVATION (reservation_id, ancien_statut, nouveau_statut, modifie_par)
    VALUES (:NEW.id, :OLD.statut, :NEW.statut, :NEW.confirme_par_id);
END;
/


-- ─── 6. PACKAGE PKG_RESERVATION ──────────────────────────────────────

CREATE OR REPLACE PACKAGE PKG_RESERVATION AS
    -- Calcule le prix total d'une réservation
    FUNCTION calculer_prix(
        p_type        IN VARCHAR2,
        p_heb_id      IN NUMBER,
        p_guide_id    IN NUMBER,
        p_date_debut  IN DATE,
        p_date_fin    IN DATE,
        p_nb_pers     IN NUMBER
    ) RETURN NUMBER;

    -- Crée une réservation complète (procédure transactionnelle)
    PROCEDURE creer_reservation(
        p_user_id    IN  NUMBER,
        p_dest_id    IN  NUMBER,
        p_type       IN  VARCHAR2,
        p_heb_id     IN  NUMBER,
        p_guide_id   IN  NUMBER,
        p_date_debut IN  DATE,
        p_date_fin   IN  DATE,
        p_nb_pers    IN  NUMBER,
        p_notes      IN  CLOB,
        p_resa_id    OUT NUMBER,
        p_erreur     OUT VARCHAR2
    );

    -- Confirme une réservation (admin)
    PROCEDURE confirmer_reservation(
        p_resa_id    IN  NUMBER,
        p_admin_id   IN  NUMBER,
        p_erreur     OUT VARCHAR2
    );

    -- Annule une réservation
    PROCEDURE annuler_reservation(
        p_resa_id    IN  NUMBER,
        p_user_id    IN  NUMBER,
        p_erreur     OUT VARCHAR2
    );
END PKG_RESERVATION;
/

CREATE OR REPLACE PACKAGE BODY PKG_RESERVATION AS

    FUNCTION calculer_prix(
        p_type        IN VARCHAR2,
        p_heb_id      IN NUMBER,
        p_guide_id    IN NUMBER,
        p_date_debut  IN DATE,
        p_date_fin    IN DATE,
        p_nb_pers     IN NUMBER
    ) RETURN NUMBER IS
        v_prix_heb   NUMBER := 0;
        v_prix_guide NUMBER := 0;
        v_nb_nuits   NUMBER;
        v_nb_jours   NUMBER;
    BEGIN
        v_nb_nuits := GREATEST(p_date_fin - p_date_debut, 1);
        v_nb_jours := GREATEST(p_date_fin - p_date_debut, 1);

        IF p_heb_id IS NOT NULL AND p_type IN ('hebergement','package') THEN
            SELECT prix_nuit INTO v_prix_heb FROM HEBERGEMENT WHERE id = p_heb_id;
            v_prix_heb := v_prix_heb * v_nb_nuits;
        END IF;

        IF p_guide_id IS NOT NULL AND p_type IN ('guide','package') THEN
            SELECT prix_journee INTO v_prix_guide FROM GUIDE WHERE id = p_guide_id;
            v_prix_guide := v_prix_guide * v_nb_jours * p_nb_pers;
        END IF;

        RETURN ROUND(v_prix_heb + v_prix_guide, 2);
    EXCEPTION
        WHEN NO_DATA_FOUND THEN RETURN 0;
    END calculer_prix;


    PROCEDURE creer_reservation(
        p_user_id    IN  NUMBER,
        p_dest_id    IN  NUMBER,
        p_type       IN  VARCHAR2,
        p_heb_id     IN  NUMBER,
        p_guide_id   IN  NUMBER,
        p_date_debut IN  DATE,
        p_date_fin   IN  DATE,
        p_nb_pers    IN  NUMBER,
        p_notes      IN  CLOB,
        p_resa_id    OUT NUMBER,
        p_erreur     OUT VARCHAR2
    ) IS
        v_id NUMBER := seq_reservation.NEXTVAL;
    BEGIN
        p_erreur := NULL;

        -- Validation dates
        IF p_date_debut < TRUNC(SYSDATE) THEN
            p_erreur := 'La date de début ne peut pas être dans le passé.';
            RETURN;
        END IF;
        IF p_date_fin <= p_date_debut THEN
            p_erreur := 'La date de fin doit être après la date de début.';
            RETURN;
        END IF;

        INSERT INTO RESERVATION (
            id, utilisateur_id, destination_id, type_reservation,
            hebergement_id, guide_id, date_debut, date_fin,
            nb_personnes, statut, notes
        ) VALUES (
            v_id, p_user_id, p_dest_id, p_type,
            p_heb_id, p_guide_id, p_date_debut, p_date_fin,
            p_nb_pers, 'en_attente', p_notes
        );

        p_resa_id := v_id;
        COMMIT;
    EXCEPTION
        WHEN OTHERS THEN
            ROLLBACK;
            p_erreur  := SQLERRM;
            p_resa_id := NULL;
    END creer_reservation;


    PROCEDURE confirmer_reservation(
        p_resa_id  IN  NUMBER,
        p_admin_id IN  NUMBER,
        p_erreur   OUT VARCHAR2
    ) IS
        v_statut VARCHAR2(20);
    BEGIN
        p_erreur := NULL;

        SELECT statut INTO v_statut FROM RESERVATION WHERE id = p_resa_id FOR UPDATE;

        IF v_statut != 'en_attente' THEN
            p_erreur := 'Seules les réservations en attente peuvent être confirmées.';
            RETURN;
        END IF;

        UPDATE RESERVATION
        SET statut = 'confirmee', confirme_par_id = p_admin_id
        WHERE id = p_resa_id;

        COMMIT;
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            p_erreur := 'Réservation introuvable.';
        WHEN OTHERS THEN
            ROLLBACK;
            p_erreur := SQLERRM;
    END confirmer_reservation;


    PROCEDURE annuler_reservation(
        p_resa_id IN  NUMBER,
        p_user_id IN  NUMBER,
        p_erreur  OUT VARCHAR2
    ) IS
        v_statut   VARCHAR2(20);
        v_user_id  NUMBER;
        v_user_role VARCHAR2(20);
    BEGIN
        p_erreur := NULL;

        SELECT r.statut, r.utilisateur_id, u.role
        INTO   v_statut, v_user_id, v_user_role
        FROM   RESERVATION r JOIN UTILISATEUR u ON u.id = p_user_id
        WHERE  r.id = p_resa_id FOR UPDATE;

        -- L'admin peut annuler n'importe quelle réservation
        IF v_user_role != 'admin' AND v_user_id != p_user_id THEN
            p_erreur := 'Vous ne pouvez annuler que vos propres réservations.';
            RETURN;
        END IF;

        IF v_statut IN ('annulee','terminee') THEN
            p_erreur := 'Cette réservation ne peut plus être annulée.';
            RETURN;
        END IF;

        UPDATE RESERVATION SET statut = 'annulee' WHERE id = p_resa_id;
        COMMIT;
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            p_erreur := 'Réservation introuvable.';
        WHEN OTHERS THEN
            ROLLBACK;
            p_erreur := SQLERRM;
    END annuler_reservation;

END PKG_RESERVATION;
/


-- ─── 7. PACKAGE PKG_STATISTIQUES ─────────────────────────────────────

CREATE OR REPLACE PACKAGE PKG_STATISTIQUES AS
    -- Retourne les statistiques globales de la plateforme
    PROCEDURE stats_globales(
        p_nb_utilisateurs OUT NUMBER,
        p_nb_reservations OUT NUMBER,
        p_revenu_total    OUT NUMBER,
        p_nb_destinations OUT NUMBER
    );

    -- Top N destinations par nombre de réservations
    FUNCTION top_destinations(p_n IN NUMBER DEFAULT 5) RETURN SYS_REFCURSOR;

    -- Top N hébergements par note
    FUNCTION top_hebergements(p_n IN NUMBER DEFAULT 5) RETURN SYS_REFCURSOR;

    -- Réservations par mois sur une année
    FUNCTION reservations_par_mois(p_annee IN NUMBER) RETURN SYS_REFCURSOR;
END PKG_STATISTIQUES;
/

CREATE OR REPLACE PACKAGE BODY PKG_STATISTIQUES AS

    PROCEDURE stats_globales(
        p_nb_utilisateurs OUT NUMBER,
        p_nb_reservations OUT NUMBER,
        p_revenu_total    OUT NUMBER,
        p_nb_destinations OUT NUMBER
    ) IS
    BEGIN
        SELECT COUNT(*) INTO p_nb_utilisateurs FROM UTILISATEUR WHERE est_actif = 1;
        SELECT COUNT(*) INTO p_nb_reservations FROM RESERVATION WHERE statut != 'annulee';
        SELECT NVL(SUM(prix_total), 0) INTO p_revenu_total FROM RESERVATION WHERE statut = 'confirmee';
        SELECT COUNT(*) INTO p_nb_destinations FROM DESTINATION WHERE est_active = 1;
    END stats_globales;


    FUNCTION top_destinations(p_n IN NUMBER DEFAULT 5) RETURN SYS_REFCURSOR IS
        v_cursor SYS_REFCURSOR;
    BEGIN
        OPEN v_cursor FOR
            SELECT d.id, d.nom, d.note_moyenne, d.nb_commentaires,
                   COUNT(r.id) AS nb_reservations
            FROM DESTINATION d
            LEFT JOIN RESERVATION r ON r.destination_id = d.id AND r.statut != 'annulee'
            WHERE d.est_active = 1
            GROUP BY d.id, d.nom, d.note_moyenne, d.nb_commentaires
            ORDER BY nb_reservations DESC, d.note_moyenne DESC
            FETCH FIRST p_n ROWS ONLY;
        RETURN v_cursor;
    END top_destinations;


    FUNCTION top_hebergements(p_n IN NUMBER DEFAULT 5) RETURN SYS_REFCURSOR IS
        v_cursor SYS_REFCURSOR;
    BEGIN
        OPEN v_cursor FOR
            SELECT h.id, h.nom, h.prix_nuit, h.note_moyenne, d.nom AS destination_nom
            FROM HEBERGEMENT h
            JOIN DESTINATION d ON d.id = h.destination_id
            WHERE h.est_actif = 1
            ORDER BY h.note_moyenne DESC, h.prix_nuit ASC
            FETCH FIRST p_n ROWS ONLY;
        RETURN v_cursor;
    END top_hebergements;


    FUNCTION reservations_par_mois(p_annee IN NUMBER) RETURN SYS_REFCURSOR IS
        v_cursor SYS_REFCURSOR;
    BEGIN
        OPEN v_cursor FOR
            SELECT EXTRACT(MONTH FROM date_creation) AS mois,
                   COUNT(*) AS nb_reservations,
                   SUM(prix_total) AS revenu_mensuel
            FROM RESERVATION
            WHERE EXTRACT(YEAR FROM date_creation) = p_annee
              AND statut != 'annulee'
            GROUP BY EXTRACT(MONTH FROM date_creation)
            ORDER BY mois;
        RETURN v_cursor;
    END reservations_par_mois;

END PKG_STATISTIQUES;
/


-- ─── 8. DONNÉES INITIALES ────────────────────────────────────────────

-- Régions de Mauritanie
INSERT INTO REGION (id, nom, description) VALUES (seq_region.NEXTVAL, 'Adrar',         'Région désertique au nord, connue pour ses ksour et ses dunes.');
INSERT INTO REGION (id, nom, description) VALUES (seq_region.NEXTVAL, 'Tagant',        'Plateau rocheux avec des oasis et des villes historiques.');
INSERT INTO REGION (id, nom, description) VALUES (seq_region.NEXTVAL, 'Hodh el Chargui','Grande région à l''est, porte du Sahara.');
INSERT INTO REGION (id, nom, description) VALUES (seq_region.NEXTVAL, 'Dakhlet Nouadhibou', 'Région côtière avec Nouadhibou, capitale économique.');
INSERT INTO REGION (id, nom, description) VALUES (seq_region.NEXTVAL, 'Trarza',        'Région du fleuve Sénégal et de Nouakchott.');
INSERT INTO REGION (id, nom, description) VALUES (seq_region.NEXTVAL, 'Assaba',        'Région centrale avec le plateau de l''Assaba.');

-- Types d'hébergement
INSERT INTO TYPE_HEBERGEMENT VALUES (1, 'Hôtel',     'fa-hotel');
INSERT INTO TYPE_HEBERGEMENT VALUES (2, 'Auberge',   'fa-bed');
INSERT INTO TYPE_HEBERGEMENT VALUES (3, 'Campement', 'fa-campground');
INSERT INTO TYPE_HEBERGEMENT VALUES (4, 'Maison d''hôtes', 'fa-home');
INSERT INTO TYPE_HEBERGEMENT VALUES (5, 'Lodge',     'fa-tree');

COMMIT;
