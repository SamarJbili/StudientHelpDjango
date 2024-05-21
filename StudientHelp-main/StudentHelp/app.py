from flask import Flask, request, jsonify

app = Flask(__name__)

# Dictionnaire pour stocker les publications avec leurs commentaires et likes
publications = {}

# Dictionnaire pour stocker les utilisateurs et leurs notifications
notifications = {}

@app.route('/publication', methods=['POST'])
def add_publication():
    data = request.json
    publication_id = data.get('id')
    content = data.get('content')
    author = data.get('author')
    publications[publication_id] = {'content': content, 'author': author, 'comments': [], 'likes': 0}
    notifications[author] = []  # Initialiser les notifications pour cet utilisateur
    return jsonify({'message': 'Publication ajoutée avec succès!'}), 201

@app.route('/publication/<publication_id>/comment', methods=['POST'])
def add_comment(publication_id):
    data = request.json
    comment = data.get('comment')
    commenter = data.get('commenter')
    if publication_id in publications:
        publications[publication_id]['comments'].append({'comment': comment, 'commenter': commenter})
        # Ajouter une notification pour l'auteur de la publication
        notifications[publications[publication_id]['author']].append(f"{commenter} a commenté votre publication.")
        return jsonify({'message': 'Commentaire ajouté avec succès!'}), 201
    else:
        return jsonify({'error': 'Publication non trouvée!'}), 404

@app.route('/publication/<publication_id>/like', methods=['POST'])
def like_publication(publication_id):
    if publication_id in publications:
        publications[publication_id]['likes'] += 1
        # Ajouter une notification pour l'auteur de la publication
        notifications[publications[publication_id]['author']].append("Quelqu'un a aimé votre publication.")
        return jsonify({'message': 'Publication aimée avec succès!'}), 201
    else:
        return jsonify({'error': 'Publication non trouvée!'}), 404

@app.route('/notifications/<user>', methods=['GET'])
def get_notifications(user):
    if user in notifications:
        user_notifications = notifications[user]
        # Effacer les notifications une fois récupérées
        notifications[user] = []
        return jsonify(user_notifications), 200
    else:
        return jsonify({'error': 'Utilisateur non trouvé!'}), 404

if __name__ == '__main__':
    app.run(debug=True)
