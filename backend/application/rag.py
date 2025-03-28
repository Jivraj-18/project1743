import os
import numpy as np
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .fs import FileManager

class QuerySelector:

    def __init__(self, model_path="model.pkl"):
        self.model_path = model_path
        self.vectorizer = None
        self.stages = {}

        if os.path.exists(self.model_path):
            with open(self.model_path, 'rb') as f:
                model_data = pickle.load(f)
                self.vectorizer = model_data['vectorizer']
                self.stages = model_data['stages']
        else:
            self.vectorizer = TfidfVectorizer(stop_words='english')

    def make_stage(self, name, data):
        """
        Takes a name for the stage and a dictionary with keys as labels and values as documents.
        Creates a stage with corresponding TF-IDF matrix and labels.
        """
        labels = list(data.keys())
        documents = [doc.lower() for doc in data.values()]
        
        # Fit and transform only once with the initial documents
        X = self.vectorizer.fit_transform(documents)

        self.stages[name] = {
            'labels': labels,
            'data': X
        }

    def update_stage(self, name, new_data):
        """
        Takes a name for the stage and a dictionary with new documents to be added,
        updates the TF-IDF matrix and labels for the corresponding stage.
        """
        # Check if the stage exists
        if name not in self.stages:
            print(f"No such stage: {name}")
            return

        stage_data = self.stages[name]
        existing_labels = stage_data['labels']
        existing_data = stage_data['data']

        # Get the new labels and documents
        new_labels = list(new_data.keys())
        new_documents = [doc.lower() for doc in new_data.values()]

        # Transform the new documents using the already fitted vectorizer
        new_X = self.vectorizer.transform(new_documents)

        # Combine old and new data (vertically stacking the TF-IDF matrices)
        combined_X = np.vstack([existing_data.toarray(), new_X.toarray()])

        # Update the stage data with new labels and combined TF-IDF matrix
        self.stages[name] = {
            'labels': existing_labels + new_labels,
            'data': combined_X
        }

    def selector(self, user_query, stage):
        """
        Takes a user query and the name of a stage,
        returns a dictionary of labels with corresponding similarity scores.
        """
        user_query = user_query.lower()

        # Check if the stage exists
        if stage not in self.stages:
            print(f"No such stage: {stage}")
            return {}

        stage_data = self.stages[stage]
        labels = stage_data['labels']
        X = stage_data['data']

        # Convert user query into TF-IDF features
        query_vector = self.vectorizer.transform([user_query])

        # Calculate cosine similarity between the user query and all documents
        cosine_similarities = cosine_similarity(query_vector, X)
        probabilities = cosine_similarities.flatten()

        # Return labels with corresponding similarity scores
        result = {label: prob for label, prob in zip(labels, probabilities)}
        b = sorted(result.items(), key=lambda x: x[1], reverse=True)

        return b



sub = FileManager('sub')
# sub.create_directory()
# sub.text_to_file('L1.txt', 'We talk about data types')
# sub.text_to_file('L2.txt', 'Lets learn about int and string')

# Setting up initial data
stageData = {}

# File data
for i in sub.files_in_dir():
    stageData[i.split(".")[0]] = sub.file_to_text(f"{i}")

# Print stage data for confirmation
for k, v in stageData.items():
    print(f"{k:<20} {v[:10]}")

# Initialize the QuerySelector class
query_selector = QuerySelector()
query_selector.make_stage("qbd", stageData)

# Add new files later
new_files = {
    "new_file1": "Content of the first new file.",
    "new_file2": "Content of the second new file."
}

# Update the existing stage with new files without retraining the vectorizer
query_selector.update_stage("qbd", new_files)

# Test the selector with the updated stage
result = query_selector.selector("What are the types of variables in python?", "qbd")

print(f"{'Label':<20} {'Probability':<10}")
print("-" * 35)

for label, prob in result:
    print(f"{label:<20} {prob:.2f}")
