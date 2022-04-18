import smtplib, ssl

def send_email(message):
	port = 465 # For SSL
	smtp_server = "smtp.gmail.com"
	sender_email = "pytestrace@gmail.com"
	password = "krtgayuyxzinfusl"
	receiver_email = "tylerrrace@gmail.com"

	context = ssl.create_default_context()
	with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
		try:
			server.login(sender_email, password)
			res = server.sendmail(sender_email, receiver_email, message)
			print("email sent")
		except:
			print("could not log in or send mail.")

send_email("test")
