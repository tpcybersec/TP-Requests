from TP_Requests import TP_Requests_VERSION
import setuptools

setuptools.setup(
	name="TP-Requests",
	version=TP_Requests_VERSION,
	author="TP Cyber Security",
	license="MIT",
	author_email="tpcybersec2023@gmail.com",
	description="Send the HTTP/ MQTT/ WEBSOCKET Request",
	long_description=open("README.md").read(),
	long_description_content_type="text/markdown",
	install_requires=open("requirements.txt").read().split(),
	url="https://github.com/tpcybersec/TP-Requests",
	classifiers=[
		"Programming Language :: Python :: 3"
	],
	keywords=["TPCyberSec", "TP_Requests", "TP_HTTP_REQUEST", "TP_MQTT_REQUEST", "TP_WEBSOCKET_REQUEST"],
	packages=setuptools.find_packages(),
)