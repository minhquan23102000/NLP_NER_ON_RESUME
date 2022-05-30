import argparse

from text_extractor import ResumeExtractor

# Instantiate the parser
parser = argparse.ArgumentParser(description='Resume ner extractor demo')

# Required positional argument
parser.add_argument('--resume_path', type=str,
                    help='Path resume to extract')
parser.add_argument('--model_path', type=str,
                    help='Spacy ner model', default='resume_ner_model/model-best', nargs='?')


args = parser.parse_args()

extractor = ResumeExtractor(args.model_path)

summary = extractor.get_summary(args.resume_path)

for key, value in summary.items():
    print(f"{key}: [{value}]")
