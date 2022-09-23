# google_calendar_notion
Get events from Google Calendar into notion Database

### Prerequisites

- [GNU Make](https://www.gnu.org/software/make/)
- [Docker](http://docker.com)

#### Google Calendar API

1. Enable Google Calendar API & Service Account
2. Create a new project.
3. Click Enable API. Search for and enable the Google Calendar API.
4. Create credentials for a Service account key.
5. Name the service account and grant it a Project Role of Owner.
6. Download the JSON file.
7. Go to IAM & Admin, Service Account, find your Service account you just created above and enable Domain-wide Delegation.

Thanks to [Muhammad Taqi](https://medium.com/@ArchTaqi/google-calendar-api-in-your-application-without-oauth-consent-screen-4fcc1f8eb380).

## RUN
```bash
make run
```