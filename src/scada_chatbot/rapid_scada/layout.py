from scada_chatbot.rapid_scada.__types__ import LayoutChapter


LAYOUT: list[LayoutChapter] = [
    {
        "title": "Overview",
        "url": "software-overview/index.html",
        "content": [
            "software-overview/introduction.html",
            "software-overview/applications.html",
            "software-overview/architecture.html",
        ],
    },
    {
        "title": "Installation",
        "url": "installation/index.html",
        "content": [
            "installation/system-requirements.html",
            "installation/install-windows.html",
            "installation/install-windows-manual.html",
            "installation/install-linux.html",
            "installation/install-modules.html",
            "installation/services.html",
            "installation/transfer.html",
            "installation/safety.html",
        ],
    },
    {
        "title": "Configuration",
        "url": "configuration/index.html",
        "content": [
            "configuration/configuration-basics.html",
            "configuration/database.html",
            "configuration/device-polling.html",
            "configuration/channels.html",
            "configuration/scripts.html",
            "configuration/views.html",
            "configuration/table-views.html",
            "configuration/user-management.html",
        ],
    },
    {
        "title": "Modules",
        "url": "modules/index.html",
        "content": [
            "modules/plg-chart-pro.html",
            "modules/plg-dashboard.html",
            "modules/plg-elastic-report.html",
            "modules/plg-map.html",
            "modules/plg-notification.html",
            "modules/mod-auto-control.html",
            "modules/mod-db-export.html",
            "modules/mod-rapid-gate.html",
            "modules/drv-db-import.html",
            "modules/drv-modbus-slave.html",
            "modules/drv-telegram.html",
        ],
    },
    {
        "title": "Additional Applications",
        "url": "additional-applications/index.html",
        "content": [
            "additional-applications/app-auto-report.html",
        ],
    },
    {
        "title": "Enterprise Edition",
        "url": "enterprise-edition/index.html",
        "content": [
            "enterprise-edition/overview.html",
            "enterprise-edition/plg-audit.html",
            "enterprise-edition/plg-guard.html",
        ],
    },
    {
        "title": "Developers",
        "url": "developers/index.html",
        "content": [
            "developers/development-basics.html",
            "developers/module-development.html",
            "developers/driver-development.html",
            "developers/plugin-development.html",
            "developers/store.html",
        ],
    },
    {
        "title": "Version History",
        "url": "version-history/index.html",
        "content": [
            "version-history/scada-history.html",
            "version-history/server-history.html",
            "version-history/communicator-history.html",
            "version-history/webstation-history.html",
            "version-history/agent-history.html",
            "version-history/administrator-history.html",
            "version-history/applications-history.html",
        ],
    },
]

ROOT_DIR = "./data/docs/rapidscada.net/docs/en/latest/"
