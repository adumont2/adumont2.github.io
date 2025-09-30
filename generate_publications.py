from pymed import PubMed
import os

# --- Configuration ---
pubmed_query = "Dumont AS[Author]"
output_file = os.path.join("_bibliography", "references.bib")

# --- Script ---
print("Connecting to PubMed...")
pubmed = PubMed(tool="MyPubmedExporter", email="your_email@example.com")
results = pubmed.query(pubmed_query, max_results=500)

print(f"Found publications. Generating BibTeX entries...")
bibtex_entries = []

for article in results:
    author_list = article.authors
    if not author_list:
        continue

    authors = " and ".join([f"{author['lastname']}, {author['firstname']}" for author in author_list])

    first_author_lastname = author_list[0]['lastname'].replace(" ", "")
    year = article.publication_date.year
    title_word = ''.join(e for e in article.title.split(' ')[0] if e.isalnum()) # Clean the title word
    citation_key = f"{first_author_lastname}{year}{title_word}"

    entry = f"""@article{{{citation_key},
    title = {{{article.title}}},
    author = {{{authors}}},
    journal = {{{article.journal}}},
    year = {{{year}}},"""

    if hasattr(article, 'volume') and article.volume:
        entry += f"\n    volume = {{{article.volume}}},"
    
    if hasattr(article, 'issue') and article.issue:
        entry += f"\n    number = {{{article.issue}}},"
        
    if hasattr(article, 'pages') and article.pages:
        entry += f"\n    pages = {{{article.pages}}},"
        
    # --- FINAL FIX IS HERE ---
    # Only take the first DOI if there are multiple lines
    if hasattr(article, 'doi') and article.doi:
        first_doi = article.doi.splitlines()[0]
        entry += f"\n    doi = {{{first_doi}}},"
    
    entry += f"\n    pmid = {{{article.pubmed_id.splitlines()[0]}}}\n}}"

    bibtex_entries.append(entry)

os.makedirs(os.path.dirname(output_file), exist_ok=True)

with open(output_file, 'w', encoding='utf-8') as f:
    f.write("\n\n".join(bibtex_entries))

print(f"Successfully generated {len(bibtex_entries)} publications in '{output_file}'")