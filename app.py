import streamlit as st
import httpx
import os

API_URL = os.environ.get("API_URL", "http://127.0.0.1:5001")

st.title("Fredagsbarens events")
st.write("Her kan du se kommende events opg ledige pladser")

try:
    response = httpx.get(f"{API_URL}/events", timeout=2)
    response.raise_for_status()
    events = response.json()

    overview = []

    for event in events:
        overview.append({
            "Titel": event["title"],
            "Dato": event["date"],
            "Antal tilmeldte": len(event["participants"]),
            "Ledige pladser": event["capacity"] - len(event["participants"])
        })

    st.dataframe(overview, hide_index=True)

except httpx.ConnectError:
    st.error("Kan ikke forbinde til API'en. Tjek om Flask kører.")

except httpx.TimeoutException:
    st.error("API'en svarer for langsomt.")

except httpx.HTTPStatusError as error:
    st.error(f"API-fejl: {error.response.status_code}")

if "name" not in st.session_state:
    st.session_state.name = ""

st.sidebar.text_input("Mit navn", key="name")

st.subheader("Tilmeld eller afmeld et event")

if "events" in locals() and events:
    selected_event = st.selectbox(
        "Vælg et event",
        events,
        format_func=lambda event: event["title"]
    )

    st.write("Deltagere:", ", ".join(selected_event["participants"]) or "Ingen endnu")

    is_full = len(selected_event["participants"]) >= selected_event["capacity"]
    name = st.session_state.name.strip()

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Tilmeld", disabled=is_full):
            if not name:
                st.error("Du skal skrive dit navn i sidebaren.")
            else:
                try:
                    response = httpx.post(
                        f"{API_URL}/events/{selected_event['id']}/signups",
                        json={"name": name},
                        timeout=2
                    )
                    response.raise_for_status()
                    st.success("Du er nu tilmeldt!")
                    st.rerun()
                except httpx.HTTPStatusError as error:
                    st.error(error.response.json().get("error", "Tilmelding mislykkedes"))
                except (httpx.ConnectError, httpx.TimeoutException):
                    st.error("Kunne ikke kontakte API'en.")

    with col2:
        if st.button("Afmeld"):
            if not name:
                st.error("Du skal skrive dit navn i sidebaren.")
            else:
                try:
                    response = httpx.delete(
                        f"{API_URL}/events/{selected_event['id']}/signups/{name}",
                        timeout=2
                    )
                    response.raise_for_status()
                    st.success("Du er nu afmeldt!")
                    st.rerun()
                except httpx.HTTPStatusError as error:
                    st.error(error.response.json().get("error", "Afmelding mislykkedes"))
                except (httpx.ConnectError, httpx.TimeoutException):
                    st.error("Kunne ikke kontakte API'en.")

st.subheader("Opret et nyt event")

with st.form("create_event_form"):
    title = st.text_input("Eventets titel")
    date = st.date_input("Dato")
    capacity = st.number_input("Antal pladser", min_value=1, step=1)

    submitted = st.form_submit_button("Opret event")

    if submitted:
        try:
            response = httpx.post(
                f"{API_URL}/events",
                json={
                    "title": title,
                    "date": str(date),
                    "capacity": int(capacity)
                },
                timeout=2
            )

            response.raise_for_status()
            st.success("Eventet er oprettet!")

        except httpx.HTTPStatusError as error:
            st.error(error.response.json().get("error", "Kunne ikke oprette eventet"))

        except httpx.ConnectError:
            st.error("Kan ikke forbinde til API'en.")

        except httpx.TimeoutException:
            st.error("API'en svarer for langsomt.")

st.subheader("Slet et event")

if "events" in locals() and events:
    event_to_delete = st.selectbox(
        "Vælg event, der skal slettes",
        events,
        format_func=lambda event: event["title"],
        key="delete_event"
    )

    if st.button("Slet event", type="primary"):
        try:
            response = httpx.delete(
                f"{API_URL}/events/{event_to_delete['id']}",
                timeout=2
            )
            response.raise_for_status()

            st.success("Eventet er slettet!")
            st.rerun()

        except httpx.HTTPStatusError as error:
            st.error(f"Kunne ikke slette eventet: {error.response.status_code}")

        except (httpx.ConnectError, httpx.TimeoutException):
            st.error("Kunne ikke kontakte API'en.")