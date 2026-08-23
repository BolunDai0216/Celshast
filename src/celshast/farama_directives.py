"""Sphinx Extensions used by Farama's projects."""

from typing import List

from docutils import nodes
from docutils.parsers.rst import Directive, directives
from docutils.parsers.rst.directives import images
from docutils.statemachine import StringList


class FaramaProjectLogoDirective(images.Figure):
    """A figure directive that tags the image as a Farama project logo."""

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        "alt": directives.unchanged,
        "height": directives.length_or_unitless,
        "width": directives.length_or_percentage_or_unitless,
        "class": directives.class_option,
    }

    def run(self) -> List[nodes.Node]:
        """Build the figure and add the project-logo class to it."""
        (img_node,) = images.Figure.run(self)
        # Add custom class to the image node.
        assert isinstance(img_node, nodes.Element)
        img_node.attributes["classes"].append("farama-project-logo")
        return [img_node]


class FaramaProjectHeadingDirective(Directive):
    """Render the directive's first content line as a project heading."""

    has_content = True

    def run(self) -> List[nodes.Node]:
        """Parse the content into a container holding an ``<h2>`` heading."""
        self.assert_has_content()

        container = nodes.container()

        html_content = StringList(
            [
                "<h2 class='farama-project-heading'>",
                self.content[0],
                "</h2>",
            ]
        )

        self.state.nested_parse(html_content, 0, container)
        return [container]
