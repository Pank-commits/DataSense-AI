from app.agents.kaggle_discovery_agent import kaggle_discovery_agent
from app.agents.metadata_agent import metadata_agent


print("\n================================")
print("KAGGLE METADATA TEST")
print("================================")

print("\nDiscovering Kaggle datasets...")

data = kaggle_discovery_agent.discover(limit=10)

print(f"\nDiscovered: {len(data)} datasets")

print("\nProcessing metadata...")

result = metadata_agent.process_batch(data)

print("\n================================")
print("KAGGLE METADATA RESULTS")
print("================================")

for dataset in result:
    print("\n--------------------------------")
    print(f"Name       : {dataset.get('name')}")
    print(f"Category   : {dataset.get('category')}")
    print(f"ML Task    : {dataset.get('ml_task')}")
    print(f"Data Type  : {dataset.get('data_type')}")
    print(f"Difficulty : {dataset.get('difficulty')}")
    print(f"License    : {dataset.get('license')}")

    confidence = dataset.get("_metadata_agent", {})

    print(
        f"Confidence : "
        f"Category={confidence.get('category_confidence')} | "
        f"ML Task={confidence.get('ml_task_confidence')} | "
        f"Data Type={confidence.get('data_type_confidence')}"
    )

print("\n================================")
print("TEST COMPLETE")
print("================================")