class TemplateService:
    @staticmethod
    def render_responsive_template(content_body: str) -> str:
        """
        Wraps campaign content into a professional, table-based HTML shell.
        This handles the CSS and layout logic for different email clients.
        """
        # Using inline CSS and Tables for maximum ESP compatibility
        base_shell = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                /* Media Queries for Mobile Responsiveness */
                @media screen and (max-width: 600px) {{
                    .container {{ width: 100% !important; }}
                }}
            </style>
        </head>
        <body style="margin: 0; padding: 0; background-color: #f6f9fc; font-family: Arial, sans-serif;">
            <table border="0" cellpadding="0" cellspacing="0" width="100%">
                <tr>
                    <td align="center" style="padding: 20px 0;">
                        <table class="container" border="0" cellpadding="0" cellspacing="0" width="600" style="background-color: #ffffff; border-radius: 8px; overflow: hidden; border: 1px solid #e1e4e8;">
                            <tr>
                                <td align="center" style="padding: 20px; background-color: #007bff; color: #ffffff;">
                                    <h2 style="margin: 0;">ASP OL Media Campaigns</h2>
                                </td>
                            </tr>
                            <tr>
                                <td style="padding: 40px; line-height: 1.6; color: #444444; font-size: 16px;">
                                    {content_body}
                                </td>
                            </tr>
                            <tr>
                                <td align="center" style="padding: 20px; background-color: #f8f9fa; color: #888888; font-size: 12px;">
                                    <p style="margin: 0;">You received this email because you're part of our list.</p>
                                    <p style="margin: 10px 0 0 0;">
                                        <a href="#" style="color: #007bff; text-decoration: none;">Unsubscribe</a> | 
                                        <a href="#" style="color: #007bff; text-decoration: none;">View in Browser</a>
                                    </p>
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