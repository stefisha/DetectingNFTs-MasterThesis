# DetectingNFTs-Master
Repository for the master thesis, regaring "Detection of scam NFTs with the use of AI"
It contains three seperate models, one based on NFT pictures, the other based on NFT descrptions and the last based on the URLs of the NFTS.
The best one proved to be the model based on pictures which is a CNN. It is hosted on https://stefisha.me/static/index.html.
The model, saved as a .keras file is hosted within a Flas app and can be called through a simple web interface, realised with HTML, CSS and a bit of vanilla JS.
The actual vm the server is deployed on is provided with Digital Ocean (a droplet), the domain and SSL certificate provided by namecheap.com. Data is collected from it with datadog.
