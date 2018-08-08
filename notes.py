import json
import pytest
import pandas as pd
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

def open_tsv_as_df(path):
    df = pd.DataFrame.from_csv(path, sep='\t')

def filter_data_by_allowed_sources(df)
    ## Psuedo-code for how to engest data
    # For each unique perferred name:
    #     for each record in the of the four accepted sources:
    #         collect the names as synonyms
    #         store a record in a new format

    # For performance, reduce the dataset to only what we're interested in. Also group by type so we don't have to do it later.
    df_gene = df[df.Source.isin(['Gene Name'])]
    df_syn = df[df.Source.isin(['Synonym'])]
    df_entry = df[df.Source.isin(['UniProt Entry'])]
    df_short = df[df.Source.isin(['UniProt_short_name'])]
    gene_uni_perf_names = df_gene.index.unique()
    syn_uni_perf_names = df_syn.index.unique()
    entry_uni_perf_names = df_entry.index.unique()
    short_uni_perf_names = df_short.index.unique()
    unique_names_by_type = [gene_uni_perf_names, syn_uni_perf_names, entry_uni_perf_names, short_uni_perf_names]
    df_by_type = [df_gene, df_syn, df_entry, df_short]

    return (unique_names_by_type, df_by_type)


def tabular_to_objects(unique_names_by_type, df_by_type)
    ## Reorganize data structure from tabular to object form
    #
    # Example tabular input:
    # Preferred_Name  Source  Name    Organism    Name_lc lengh
    # Q95TU2  RefSeq mRNA ID  NM_164977   Drosophila  nm_164977   9
    # Q95TU2  EMBL    AY058525    Drosophila  ay058525    8
    #
    # Example object output: 
    # [{'Gene Name': 'CELE_Y60C6A.2',
    #   'Perferred_Same': 'Q7SXH5',
    #   'synonyms': ['CELE_Y60C6A.2', 'E3CTH1_CAEEL']},
    #  {'Gene Name': 'E3CTH1_CAEEL',
    #   'Perferred_Same': 'Q7SXH5',
    #   'synonyms': ['CELE_Y60C6A.2', 'E3CTH1_CAEEL']}]
    objects = []
    for unique_names, df_subset in zip(unique_names_by_type, df_by_type):
        for perferred_name in unique_names:
            subset = df_subset[(df_subset.index == perferred_name)]
            synonyms = list(subset.Name)

            for index, row in subset.iterrows():
                record = {
                    "Gene Name": row.Name,
                    "Perferred_Name": perferred_name,
                    "synonyms": synonyms
                }
                objects.append(record)

    return objects


def etl():
    df = open_tsv_as_df('data/Data.tsv')
    unique_names_by_type, df_by_type = filter_data_by_allowed_sources(df)
    objects = tabular_to_objects(unique_names_by_type, df_by_type)

    # Write to temp json file
    objects_json = json.dumps(objects)
    with open("data/data.json", 'a') as fout:
       fout.write(objects_json)


# Insert into MongoDB 
# http://api.mongodb.com/python/current/tutorial.html



# Relational database Setup 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/daniel/assessment/data/test.db'
db = SQLAlchemy(app)

# Database models
class Gene(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    perferred_name = db.Column(db.String(120))
    synonyms = db.Column(db.String(120))

    db.relationship('Category',
        backref=db.backref('posts', lazy=True))


    def __repr__(self):
        return '<Gene %r>' % self.username

# Create and insert to database
from yourapplication import db
db.create_all()
db.session.add(gene)
db.session.commit()
Gene.query.filter_by(name='BP').first()


# Web routes
@app.route('/')
def main():
    html == """<form action="/request" method="post">
        <input type="text" name="gene_name">
        <input type="submit">
    </form>"""
    return html

@app.route('/request', methods=['POST'])
def handle_data():
    """Will return all information about a gene requested by name"""
    gene_name = request.form['gene_name']
    # Lookup in databases


# Tests
def test_near_hundred():
    assert(near_hundered(93)==True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
