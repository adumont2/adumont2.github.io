from pymed import PubMed
import os

# --- Configuration ---
# Create a detailed query to ensure you only get your publications.
# Use your full name, and if needed, add your affiliation to avoid
# name conflicts. Example: "(Dumont AS[Author]) AND (Tulane[Affiliation])"
pubmed_query = "Dumont AS[Author]"
output_file = os.path.join("_bibliography", "references.bib")

# --- Script ---
print("Connecting to PubMed...")
pubmed = PubMed(tool="MyPubmedExporter", email="your_email@example.com")
results = pubmed.query(pubmed_query, max_results=500)

print(f"Found publications. Generating BibTeX entries...")
bibtex_entries = []

for article in results:
    # The library stores authors as a list of dictionaries
    author_list = article.authors
    authors = " and ".join([f"{author['lastname']}, {author['firstname']}" for author in author_list])

    # Create the BibTeX citation key (e.g., Dumont2025Title)
    first_author_lastname = author_list[0]['lastname'].replace(" ", "")
    year = article.publication_date.year
    title_word = article.title.split(' ')[0].capitalize()
    citation_key = f"{first_author_lastname}{year}{title_word}"

    # Build the BibTeX entry string
    entry = f"""@article{{{citation_key},
    title = {{{article.title}}},
    author = {{{authors}}},
    journal = {{{article.journal}}},
    year = {{{year}}},
    volume = {{{article.volume}}},
    number = {{{article.issue}}},
    pages = {{{article.pages}}},
    doi = {{{article.doi}}},
    pmid = {{{article.pubmed_id.splitlines()[0]}}}
}}"""
    bibtex_entries.append(entry)

# Ensure the _bibliography directory exists
os.makedirs(os.path.dirname(output_file), exist_ok=True)

# Write all entries to the output file
with open(output_file, 'w', encoding='utf-8') as f:
    f.write("\n\n".join(bibtex_entries))

print(f"Successfully generated {len(bibtex_entries)} publications in '{output_file}'")