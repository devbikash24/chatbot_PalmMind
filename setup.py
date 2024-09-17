from setuptools import setup, find_packages

# Load the README.md for the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="conversational_chatbot",  # Replace with your project name
    version="0.1.0",  # Initial version of your project
    author="Bikash Dev",  # Replace with your name
    author_email="devbikash24@gmail.com",  # Replace with your email
    description="""

     a Chatbot that can answer user queries from any documents and add a conversational form for collecting user information (Name, Phone Number, Email) when user ask chatbot to call them, You can use LangChain & Gemini/or any LLMs to complete the project.

Also, integrate conversational form (book appointment) with tool-agents. Integration of  conversational form with agent-tools, extract complete date format like (YYYY-MM-DD) from users query (eg. Next Monday, and integrate validation in user input with conversational form (like email, phone number) etc.
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
