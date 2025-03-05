import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class QuerySelector:

    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.stages = {}

    def make_stage(self, name, data):
        """
        Takes a name for the stage and a dictionary with keys as labels and values as documents.
        Creates a stage with corresponding TF-IDF matrix and labels.
        """
        labels = list(data.keys())
        documents = [doc.lower() for doc in data.values()]
        X = self.vectorizer.fit_transform(documents)

        self.stages[name] = {
            'labels': labels,
            'data': X
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
        return result


python = FileManager('python')
python.create_directory()
python.text_to_file('L1.txt', 'We talk about data types')
python.text_to_file('L2.txt', 'Lets learn about int and string')


# Setting Up data
stageData = {}

# File data
for i in python.files_in_dir():
    stageData[i.split(".")[0]] = python.file_to_text(f"{i}")



# Manual data
stageData["sb"] =  """A magne motors and generators. The interaction of magnetic fields in electric devices such as transformers is conceptualized and investigated as magnetic circuits. Magnetic forces give information about the charge carriers in a material through the Hall effect. The Earth produces its own magnetic field, which shields the Earth's ozone layer from the solar wind and is important in navigation using a compass."""
stageData["quantum"] =  """A quantum computer is a computer that exploits quantum mechanical phenomena. ufficiently isolated can solve the same computational problems as a quantum computer, given enough time. Quantum advantage comes in the form of time complexity rather than computability, and quantum complexity theory shows that some quantum algorithms are exponentially more efficient than the best-known classical algorithms. A large-scale quantum computer could in theory solve computational problems unsolvable by a classical computer in any reasonable amount of time. This concept of extra ability has been called "quantum supremacy". While such claims have drawn significant attention to the discipline, near-term practical use cases remain limited."""
stageData["Hydrogen"] =  """Hydrogen is a chemical element; The more familiar electrolysis of water is uncommon because it is energy-intensive, i.e. expensive.[16][17] Its main industrial uses include fossil fuel processing, such as hydrocracking and hydrodesulfurization. Ammonia production also is a major consumer of hydrogen. Fuel cells for electricity generation from hydrogen is rapidly emerging.[18]"""

# print(stageData)
for k, v in stageData.items():
    print(f"{k:<20} {v[:10]}")

# Initialize the class
query_selector = QuerySelector()
query_selector.make_stage("qbd", stageData)

# Testing
result = query_selector.selector("What do you mean by computer motors", "qbd")
sorted_result = sorted(result.items(), key=lambda x: x[1], reverse=True)

print(f"{'Label':<20} {'Probability':<10}")
print("-" * 35)

for label, prob in sorted_result:
    print(f"{label:<20} {prob:.2f}")