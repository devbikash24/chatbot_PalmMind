import os
import yaml
import logging
from dotenv import load_dotenv
from pyprojroot import here

# Setup logging configuration
logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s')

# Load environment variables
if load_dotenv():
    logging.info("Environment variables loaded successfully.")


class LoadConfiguration:
    """
    A class for loading configuration settings and managing directories.

    This class loads various configuration settings from the 'config.yaml' file,
    including language model (LLM) configurations, splitting configuration and memory configurations. 

    Attributes:
        directories_for_doc (str): Directories for document storage as specified in the config.
        persistent_directory (str): Directory for persistent storage.
        chunk_size (int): Chunk size for document splitting as specified in the config.
        chunk_overlap (int): Overlap size for document splitting.
        model (str): Embedding model name.
        top_k (int): Top K embeddings to retrieve.
        model_name (str): Name of the LLM model.
        llm_system_role (str): Role description for the LLM system.
        temperature (float): Temperature setting for the LLM model.
        max_tokens (int): Maximum token limit for the LLM model.
        number_of_q_a_pairs (int): Number of Q&A pairs to be stored in memory.

    Methods:
        load_directories(app_config):
            Loads the directory configurations from the configuration file.
        load_splitter_config(app_config):
            Loads the document splitter configurations.
        load_embedding_config(app_config):
            Loads the embedding model configurations.
        load_llm_configs(app_config):
            Loads the LLM model configurations.
        load_chat_memory(app_config):
            Loads memory configuration settings for chat applications.
    """

    def __init__(self) -> None:
        """
        Initializes LoadConfiguration class by reading the configuration file and
        loading various configuration sections.
        """
        try:
            config_path = here("configuration/config.yaml")
            with open(config_path, encoding="utf-8") as file:
                app_config = yaml.safe_load(file)

            logging.info("Configuration file loaded successfully.")

            # Load configurations
            self.load_directories(app_config)
            self.load_splitter_config(app_config)
            self.load_embedding_config(app_config)
            self.load_llm_configs(app_config)
            self.load_chat_memory(app_config)

        except FileNotFoundError:
            logging.error(f"Configuration file not found at {config_path}.")
        except yaml.YAMLError as err:
            logging.error(f"Error parsing YAML file: {err}")

    def load_directories(self, app_config: dict) -> None:
        """
        Load directory configurations.

        Args:
            app_config (dict): Configuration dictionary loaded from YAML file.
        """
        self.directories_for_doc = here() / app_config['directories']['directories_for_docs']
        self.persistent_directory = here() / app_config['directories']['persist_directory']
        logging.info("Directories loaded successfully.")

    def load_splitter_config(self, app_config: dict) -> None:
        """
        Load document splitter configuration.

        Args:
            app_config (dict): Configuration dictionary loaded from YAML file.
        """
        self.chunk_size = app_config['splitter_config']['chunk_size']
        self.chunk_overlap = app_config['splitter_config']['chunk_overlap']
        logging.info("Splitter configuration loaded successfully.")

    def load_embedding_config(self, app_config: dict) -> None:
        """
        Load embedding model configuration.

        Args:
            app_config (dict): Configuration dictionary loaded from YAML file.
        """
        self.embedding_model = app_config['embeddings']['model']
        self.top_k = app_config['embeddings']['top_k']
        logging.info("Embedding configuration loaded successfully.")

    def load_llm_configs(self, app_config: dict) -> None:
        """
        Load LLM (Language Learning Model) configuration.

        Args:
            app_config (dict): Configuration dictionary loaded from YAML file.
        """
        self.llm_model = app_config["llm_config"]["model_name"]
        self.llm_system_role = app_config["llm_config"]["llm_system_role"]
        self.temperature = app_config["llm_config"]["temperature"]
        self.max_tokens = app_config['llm_config']['max_tokens']
        logging.info("LLM configuration loaded successfully.")

    def load_chat_memory(self, app_config: dict) -> None:
        """
        Load chat memory configuration settings.

        Args:
            app_config (dict): Configuration dictionary loaded from YAML file.
        """
        self.number_of_q_a_pairs = app_config["memory"]["number_of_q_a_pairs"]
        logging.info("Chat memory configuration loaded successfully.")


# Instantiate the configuration loader
if __name__ == "__main__":
    config_loader = LoadConfiguration()

    # Example: Access and print attributes
    print(config_loader.directories_for_doc)
    print(config_loader.llm_system_role)
