// keycloak.ts
import Keycloak, { KeycloakInstance } from 'keycloak-js';

const keycloakConfig = {
  realm: 'your-realm',
  url: 'https://your-keycloak-server/auth',
  clientId: 'your-vue-client-id',
};

const keycloak: KeycloakInstance = Keycloak(keycloakConfig);

export default keycloak;
