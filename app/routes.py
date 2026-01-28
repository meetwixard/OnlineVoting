from flask import Blueprint, request, jsonify
from .models import db, Voter, Ballot

vote_bp = Blueprint('vote', __name__)

@vote_bp.route('/cast-vote', methods=['POST'])
def cast_vote():
    data = request.get_json()
    voter_id = data.get('voter_id')
    selection = data.get('candidate')

    if not voter_id or not selection:
        return jsonify({"status": "error", "message": "Invalid request payload"}), 400

    try:
        # 1. LOCK THE RECORD: This prevents race conditions.
        # No other process can read or write to this voter row until we commit.
        voter = Voter.query.with_for_update().filter_by(id=voter_id).first()

        if not voter:
            return jsonify({"status": "error", "message": "Voter not found"}), 404

        # 2. VALIDATE ELIGIBILITY
        if voter.has_voted:
            return jsonify({"status": "denied", "message": "Credential already used."}), 403

        # 3. RECORD ANONYMOUS BALLOT
        new_ballot = Ballot(candidate_id=selection)
        db.session.add(new_ballot)

        # 4. MARK CREDENTIAL AS SPENT
        voter.has_voted = True
        
        # 5. ATOMIC COMMIT
        # Both the Ballot and the Voter update succeed or fail together.
        db.session.commit()

        return jsonify({"status": "success", "message": "Vote verified and cast."}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "critical_failure", "message": str(e)}), 500
