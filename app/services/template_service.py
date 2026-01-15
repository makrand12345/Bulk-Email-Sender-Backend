from jinja2 import Template

class TemplateService:
    @staticmethod
    def render_template(content: dict, context: dict) -> str:
        """
        Renders campaign content into a single fixed email layout.
        Works for any company.
        """

        body_template = Template(content["body"])
        rendered_body = body_template.render(context)

        base_shell = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="margin:0;padding:0;background:#f6f9fc;font-family:Arial,sans-serif;">
            <table width="100%" cellpadding="0" cellspacing="0">
                <tr>
                    <td align="center" style="padding:20px">
                        <table width="600" cellpadding="0" cellspacing="0"
                               style="background:#ffffff;border-radius:8px;overflow:hidden;">
                            
                            <!-- Header -->
                            <tr>
                                <td style="padding:20px;background:#0d6efd;color:#ffffff;text-align:center;">
                                    <h2 style="margin:0;">{content["company_name"]}</h2>
                                    <p style="margin:5px 0 0 0;font-size:14px;">
                                        {content["header_title"]}
                                    </p>
                                </td>
                            </tr>

                            <!-- Body -->
                            <tr>
                                <td style="padding:30px;color:#333;font-size:16px;line-height:1.6;">
                                    <h3 style="margin-top:0;">{content["title"]}</h3>
                                    {rendered_body}
                                </td>
                            </tr>

                            <!-- Footer -->
                            <tr>
                                <td style="padding:15px;background:#f1f1f1;
                                           font-size:12px;color:#777;text-align:center;">
                                    {content["footer"]}
                                </td>
                            </tr>

                        </table>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """
        return base_shell
