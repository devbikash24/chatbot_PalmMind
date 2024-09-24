from setuptools import setup, find_packages

# Load the README.md for the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="conversational_chatbot", 
    version="0.1.0", 
    author="Bikash Dev",  
    author_email="devbikash24@gmail.com", 
    description="""
Develop a chatbot capable of answering user queries based on any uploaded documents while incorporating a conversational form to collect user information (such as Name, Phone Number, and Email) when the user requests a callback. The project leverages LangChain and Gemini (or any suitable large language models) to handle the chatbot's functionality.

Additionally, the chatbot integrates a conversational form for booking appointments, utilizing tool agents to manage this process. The form also extracts full date formats (e.g., YYYY-MM-DD) from user queries, such as "Next Monday," and validates user inputs like email addresses and phone numbers to ensure accuracy and completeness.
     
""",  # Short description
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/devbikash24/chatbot_PalmMind",  
    packages=find_packages(),  # Automatically find all packages in your project
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "pydantic>=1.8.2",
        "python-dotenv>=0.19.0",
        "pyyaml>=5.4.1",
        "huggingface-hub>=0.0.12",
        "faiss-cpu>=1.7.1",
        "langchain>=0.0.67",
        "dateutil",
        "pyprojroot",
        "setuptools>=42",  # Ensure setuptools is up to date
    ],
    entry_points={
        "console_scripts": [
            "your_project_name=your_package_name.main:main",  # Optional command-line entry point
        ],
    },
    include_package_data=True,  # Automatically include files specified in MANIFEST.in
)
