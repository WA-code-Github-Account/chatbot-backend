import traceback
from qdrant_client import QdrantClient
from config.settings import settings

print('Qdrant Host:', settings.qdrant_host)
print('Qdrant API Key present:', bool(settings.qdrant_api_key))

try:
    # Check if protocol is missing and add it if needed
    qdrant_host = settings.qdrant_host
    if not qdrant_host.startswith('http://') and not qdrant_host.startswith('https://'):
        qdrant_host = 'https://' + qdrant_host
        print('Added protocol, new host:', qdrant_host)

    print('Connecting to Qdrant...')
    
    client = QdrantClient(
        url=qdrant_host,
        api_key=settings.qdrant_api_key,
        prefer_grpc=False
    )
    
    # Try to get collections to test the connection
    collections = client.get_collections()
    print('Successfully connected to Qdrant')
    print('Collections:', [col.name for col in collections.collections])
except Exception as e:
    print('Error connecting to Qdrant:', str(e))
    print('Full traceback:')
    traceback.print_exc()