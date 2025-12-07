from setuptools import setup, find_packages

setup(
    name="agent-system",
    version=open("VERSION").read().strip(),
    description="Multi-agent AI workflow coordination system",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        # No external dependencies - using Python standard library
    ],
    entry_points={
        "console_scripts": [
            "agent-system=agent_system.cli:main",
        ],
    },
)