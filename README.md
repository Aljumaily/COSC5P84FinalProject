# Extending debias_NLG

This is an extension, done by Anuththara Lekamalage, Yiduo Zhang and Maysara Al Jumaily, of the implementation of "A Parameter-Efficient Multi-Objective Approach to Mitigate Stereotypical Bias in Language Models". The authors have incorporated multiple probability alignment objectives to achieve comprehensive bias mitigations while maintaining language abilities of generative language models. We extended the work to also include a French dataset and Spanish dataset. However, the Spanish implementation is not complete but the dataset exist.

To execute the program, use one of the three `langauge` parameters:
```
py main.py --language=en
py main.py --language=fr
py main.py --language=fr-en

```
