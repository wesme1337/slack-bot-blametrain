import os
import json
import re

from flask import Flask, jsonify, request, abort

app = Flask(__name__)

with open('config.json') as config_file:
	config = json.load(config_file)

def is_request_valid(request):
	is_token_valid = request.form['token'] == config.get("SLACK_VERIFICATION_TOKEN")
	is_team_id_valid = request.form['team_id'] == config.get("SLACK_TEAM_ID")

	return is_token_valid and is_team_id_valid


@app.route('/blametrain', methods=['POST'])
def blame_train():
	if not is_request_valid(request):
		abort(400)

	words = request.form.get('text', None).split()

	if len(words) < 2:
		return jsonify(
			response_type='ephemeral',
			text='The blame train requires a conductor and passenger. Please use two arguments with the /blame command.'
		)

	conductor = words[0]
	passenger = words[1]

	if (not re.match("\\:", conductor) and not re.match("\\:", passenger)):
		return jsonify(
			response_type='ephemeral',
			text='Only slack emojis are supported at this time. Please use an emoji to blame someone.'
		)

	return jsonify(
		response_type='in_channel',
		text=f':dumpsterfire:                                                                  :firepoop:\n:blame:                                                                  :blame:\n:blame:                                                                    :blame:\n:blame: :blame: :blame: :blame: :blame: :blame: :blame: :blame: :blame: :blame: :blame: :blame: :blame: :blame: :blame::blame:\n:blame: {passenger}  :blame: :blame: :blame: :blame: :blame: :blame: :blame: :blame: :blame: :blame: :blame: :blame: {conductor} :blame:\n:blame: :blame: :blame: :blame: :blame: :blame: :blame: :blame: :blame: :blame: :blame: :blame: :blame: :blame: :blame::blame:\n:blame::red_circle::red_circle::red_circle: :blame: :blame: :blame: :blame: :blame: :blame: :blame: :blame: :blame: :red_circle: :red_circle: :red_circle: :blame:',
	)
