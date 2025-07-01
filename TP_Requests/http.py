import socket, ssl, time
from TP_HTTP_Request_Response_Parser import TP_HTTP_REQUEST_PARSER, TP_HTTP_RESPONSE_PARSER

class TP_HTTP_REQUEST:
	def __init__(self, rawRequest:str, Coding="utf-8", separator:str="||", parse_index:str="$", dupSign_start:str="{{{", dupSign_end:str="}}}", ordered_dict:bool=False, skipDuplicated:bool=True) -> None:
		self.__version = "2025.7.1"
		self.separator = separator
		self.parse_index = parse_index
		self.dupSign_start = dupSign_start
		self.dupSign_end = dupSign_end
		self.ordered_dict = ordered_dict
		self.skipDuplicated = skipDuplicated

		self.Coding = Coding
		self.RequestParser = TP_HTTP_REQUEST_PARSER(rawRequest, separator=self.separator, parse_index=self.parse_index, dupSign_start=self.dupSign_start, dupSign_end=self.dupSign_end, ordered_dict=self.ordered_dict, skipDuplicated=self.skipDuplicated)

		if self.RequestParser.request_headers.get("User-Agent", case_insensitive=True)["value"] == "JSON_DUPLICATE_KEYS_ERROR":
			self.RequestParser.request_headers.set("User-Agent", "TP-Requests (http/TP_HTTP_REQUEST "+self.__version+")")
		if self.RequestParser.request_headers.get("Connection", case_insensitive=True)["value"] == "JSON_DUPLICATE_KEYS_ERROR":
			self.RequestParser.request_headers.set("Connection", "close")


	def sendRequest(self, Host:str, Port:int, Scheme:str, ReqTimeout:int=60, update_content_length:bool=True, proxy_server:dict=None) -> dict:
		rawRequest = self.RequestParser.unparse(update_content_length=update_content_length)
		rawResponse = b""
		request_timestamp = response_timestamp = 0

		try:
			# Create a socket connection
			client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			client_socket.settimeout(ReqTimeout)

			# Connect to the proxy/ server
			if type(proxy_server) == dict:
				client_socket.connect((proxy_server["host"], proxy_server["port"]))
			else:
				client_socket.connect((Host, Port))

			# Perform SSL/TLS handshake with the target server
			if Scheme == "https":
				context = ssl.create_default_context()
				context.check_hostname = False
				context.verify_mode = ssl.CERT_NONE
				client_socket = context.wrap_socket(client_socket, server_side=False, server_hostname=Host)

			request_timestamp = int(time.time()*1000)

			# Send the HTTP request
			client_socket.sendall(rawRequest.encode(self.Coding))

			# Receive and process the server's response
			startReceivedResponse = True
			while True:
				chunk = client_socket.recv(4096)
				if startReceivedResponse: response_timestamp = int(time.time()*1000)
				if not chunk:
					break
				rawResponse += chunk
				startReceivedResponse = False

			# Close the connections
			client_socket.close()
		except Exception as e:
			pass

		rawResponse = TP_HTTP_RESPONSE_PARSER(rawResponse, separator=self.separator, parse_index=self.parse_index, dupSign_start=self.dupSign_start, dupSign_end=self.dupSign_end, ordered_dict=self.ordered_dict, skipDuplicated=self.skipDuplicated).unparse(update_content_length=True) if len(rawResponse) > 0 else ""

		return {
			"Host": Host,
			"Port": Port,
			"Scheme": Scheme,
			"rawRequest": rawRequest,
			"rawResponse": rawResponse,
			"RequestTime": response_timestamp - request_timestamp
		}