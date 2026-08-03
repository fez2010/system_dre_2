
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection

# 1. Connexion au serveur Milvus
connections.connect("default", host="localhost", port="19530")

# 2. Définition du schéma (Signature Acoustique + Lexique)
fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=128), # dim de hidden_dim
    FieldSchema(name="label", dtype=DataType.VARCHAR, max_length=100),    # Monde lexical
    FieldSchema(name="type_donnee", dtype=DataType.VARCHAR, max_length=20) # 'réelle' ou 'artificielle'
]

schema = CollectionSchema(fields, "Base de connaissances pour AudioNlpImuFusionNet")
collection = Collection("acoustique_rag", schema)

# 3. Création de l'index pour une recherche ultra-rapide (IVF_FLAT ou HNSW)
index_params = {
    "metric_type": "L2", # Distance euclidienne pour la branche siamoise
    "index_type": "HNSW",
    "params": {"M": 8, "efConstruction": 64}
}
collection.create_index(field_name="embedding", index_params=index_params)ex