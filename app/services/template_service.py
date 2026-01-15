from jinja2 import Template

class TemplateService:
    @staticmethod
    def render_template(content: dict, context: dict) -> str:
        body_template = Template(content["body"])
        rendered_body = body_template.render(context)

        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="margin:0;padding:0;background:#f3f7f4;font-family:Arial,sans-serif;">
            <table width="100%" cellpadding="0" cellspacing="0">
                <tr>
                    <td align="center" style="padding:30px">
                        <table width="600" cellpadding="0" cellspacing="0"
                               style="background:#ffffff;border-radius:10px;overflow:hidden;
                                      box-shadow:0 4px 12px rgba(0,0,0,0.08);">

                            <!-- Header -->
                            <tr>
                                <td align="center"
                                    style="padding:24px;background:#1b5e20;color:#ffffff;">
                                    <h2 style="margin:0;font-weight:600;">
                                        {content["company_name"]}
                                    </h2>
                                    <p style="margin:6px 0 0 0;font-size:14px;opacity:0.9;">
                                        {content["header_title"]}
                                    </p>
                                </td>
                            </tr>

                            <!-- Body -->
                            <tr>
                                <td style="padding:40px;color:#2f3e34;
                                           font-size:16px;line-height:1.7;text-align:left;">
                                    <h3 style="margin-top:0;text-align:center;
                                               font-weight:600;color:#1b5e20;">
                                        {content["title"]}
                                    </h3>
                                    <div style="margin-top:20px;">
                                        {rendered_body}
                                    </div>
                                </td>
                            </tr>

                            <!-- Footer -->
                            <tr>
                                <td align="center"
                                    style="padding:18px;background:#eef4ef;
                                           font-size:12px;color:#5f6f64;">
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
