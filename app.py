import streamlit as st
import streamlit.components.v1 as components
from groq import Groq

# -------------------------
# CONFIGURATION DE LA PAGE
# -------------------------
st.set_page_config(page_title="PhoneScript Pro", page_icon="📞", layout="wide")

# Design épuré et suppression de la sidebar
st.markdown("""
<style>
[data-testid="stSidebar"] {display: none !important;}
[data-testid="stSidebarNav"] {display: none !important;}
@import url('https://googleapis.com');
html, body, div, p, h1, h2, h3, h4, h5, h6, span {
    font-family: 'Poppins', sans-serif !important;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# CONFIGURATION PAYPAL
# -------------------------
PAYPAL_CLIENT_ID = "DEMO"  
PAYPAL_PLAN_ID = "DEMO"    

# -------------------------
# GESTION DE L'ACCÈS
# -------------------------
if "est_abonne" not in st.session_state:
    st.session_state.est_abonne = False

try:
    API_KEY = st.secrets["GROQ_API_KEY"]
except:
    API_KEY = ""

# -------------------------
# INTERFACE SÉCURISÉE
# -------------------------
st.title("📞 PhoneScript Pro")
st.subheader("Générez des scripts de prospection téléphonique et détruisez les objections en 2 secondes.")

# CAS 1 : L'UTILISATEUR N'A PAS PAYÉ
if not st.session_state.est_abonne:
    st.warning("🔒 Cette application est réservée aux membres de la version Premium.")
    
    col_offre, col_connexion = st.columns(2, gap="large")
    
    with col_offre:
        st.subheader("🚀 Multipliez vos rendez-vous pour 30 $/mois")
        st.write("Ne bégayez plus jamais au téléphone. Obtenez des scripts de cold calling précis et des techniques imparables pour franchir le barrage des secrétaires.")
        st.write("Le paiement est entièrement sécurisé par **PayPal**.")
        
        if PAYPAL_CLIENT_ID == "DEMO":
            paypal_html = """
            <a href="https://paypal.com" target="_blank" style="text-decoration: none;">
                <div style="background-color: #ffc439; color: #003087; text-align: center; 
                            padding: 12px; font-family: Arial, sans-serif; font-weight: bold; 
                            border-radius: 4px; max-width: 300px; cursor: pointer; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    🟨 S'abonner avec PayPal (Démo)
                </div>
            </a>
            """
        else:
            paypal_html = f"""
            <div id="paypal-button-container-fixed" style="max-width: 350px; margin-top: 20px;"></div>
            <script src="https://paypal.com/sdk/js?client-id={PAYPAL_CLIENT_ID}&vault=true&intent=subscription" data-sdk-integration-source="button-factory"></script>
            <script>
              paypal.Buttons({{
                  style: {{ shape: 'rect', color: 'gold', layout: 'vertical', label: 'subscribe' }},
                  createSubscription: function(data, actions) {{
                    return actions.subscription.create({{ 'plan_id': '{PAYPAL_PLAN_ID}' }});
                  }},
                  onApprove: function(data, actions) {{
                    alert('Abonnement réussi ! ID : ' + data.subscriptionID);
                  }}
              }}).render('#paypal-button-container-fixed');
            </script>
            """
        components.html(paypal_html, height=150, scrolling=False)
        
    with col_connexion:
        st.subheader("🔑 Déjà abonné ?")
        email = st.text_input("Adresse e-mail")
        mot_de_passe = st.text_input("Mot de passe", type="password")
        
        if st.button("Se connecter", use_container_width=True):
            if email == "test@client.com" and mot_de_passe == "phone30":
                st.session_state.est_abonne = True
                st.success("Accès accordé !")
                st.rerun()
            else:
                st.error("Identifiants incorrects.")

# CAS 2 : L'UTILISATEUR EST ABONNÉ -> ACCÈS COMPLÈT
else:
    st.write("✨ **Espace Commercial Actif.** Décrochez vos prochains contrats.")
    if st.button("🚪 Se déconnecter", key="logout"):
        st.session_state.est_abonne = False
        st.rerun()
        
    st.write("---")

    with st.container(border=True):
        col_inputs, col_options = st.columns(2)
        
        with col_inputs:
            produit_service = st.text_input("Que vendez-vous ? (Produit ou service) :", placeholder="Ex: Création de sites web pour artisans, Panneaux solaires")
            cible = st.text_input("Qui appelez-vous ? (Votre cible) :", placeholder="Ex: Gérants de restaurants, Directeurs Immobiliers")
            offre_valeur = st.text_area(
                "Votre promesse / avantage clé :", 
                placeholder="Ex: Nous leur créons un site en 7 jours pour doubler leurs réservations en ligne."
            )
            
        with col_options:
            type_script = st.selectbox("Objectif principal de l'appel", [
                "🎯 Script de Cold Calling complet (Décrocher un rendez-vous)",
                "🛡️ Passer le barrage de la secrétaire / standardiste",
                "⚡ Traitement d'une objection précise (C'est trop cher, Pas le temps)",
                "🔥 Script de Relance (Client qui a reçu une proposition)"
            ])
            
            objection_cible = st.selectbox("Sélectionnez l'objection majeure à traiter (Optionnel)", [
                "Aucune (Générer le script standard)",
                "Envoyer un e-mail / Je n'ai pas le temps",
                "Je n'ai pas de budget / C'est trop cher",
                "Nous avons déjà un prestataire et tout va bien",
                "Je dois en parler à mon associé / y réfléchir"
            ])

        generer = st.button("🚀 Générer le Script de Vente Élite", use_container_width=True)

    if generer:
        if not API_KEY:
            st.error("⚠️ Erreur : La clé GROQ_API_KEY est manquante dans les Secrets.")
        elif not produit_service or not cible:
            st.error("⚠️ Veuillez remplir le produit vendu et la cible.")
        else:
            with st.spinner("L'IA de Groq structure votre script d'appel téléphonique..."):
                try:
                    client = Groq(api_key=API_KEY)
                    
                    prompt_systeme = """Tu es un directeur commercial d'élite et le meilleur formateur en cold calling au monde.
                    Ton but est de concevoir des guides d'appels téléphoniques extrêmement percutants, fluides et naturels.
                    Ne donne pas de répliques robotiques. Écris des phrases courtes, faciles à prononcer à l'oral.
                    Structure le script sous forme de dialogue avec des sections claires :
                    1. **L'Accroche (Les 15 premières secondes pour casser la garde)**
                    2. **La Proposition de valeur (Donner envie d'en savoir plus)**
                    3. **Le Traitement des Objections principales (Contrer les refus avec psychologie)**
                    4. **La Prise de rendez-vous (La fermeture / l'appel à l'action)**
                    Ne fais aucune introduction ni conclusion amicale, commence directement par le script."""

                    prompt_utilisateur = f"""
                    Produit/Service vendu : {produit_service}
                    Public ciblé : {cible}
                    Avantage majeur : {offre_valeur}
                    Type de document souhaité : {type_script}
                    Objection critique à désamorcer : {objection_cible}
                    """

                    reponse = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": prompt_systeme},
                            {"role": "user", "content": prompt_utilisateur}
                        ],
                        temperature=0.7
                    )
                    
                    # Code d'extraction corrigé avec l'index pour éviter les bugs
                    script_final = reponse.choices.message.content
                    st.success("✨ Votre script téléphonique de pro est prêt !")
                    st.markdown(script_final)
                    st.text_area("Copier le texte brut :", value=script_final, height=300)

                except Exception as e:
                    st.error(f"Erreur technique Groq : {str(e)}")
