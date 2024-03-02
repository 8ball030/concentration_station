// @ts-nocheck
import lsp3ProfileSchema from '@erc725/erc725.js/schemas/LSP3ProfileMetadata.json' assert { type: 'json' };
import { ERC725 } from '@erc725/erc725.js'
import {SUPPORTED_LUKSO_NETWORKS} from '$lib/consts'

export const fetchProfile = async (network, account) => {
    if  (!account || !network) {
      return;
    }

    // Get the current network properties from the list of supported networks
    const currentNetwork = SUPPORTED_LUKSO_NETWORKS.find(
      (net) => net.name === network
    );

    if (!currentNetwork) {
      return;
    }

    // Instanciate the LSP3-based smart contract
    const erc725js = new ERC725(
      lsp3ProfileSchema,
      account,
      currentNetwork.rpcUrl,
      { ipfsGateway: currentNetwork.ipfsGateway }
    );

    try {
      // Download and verify the full profile metadata
      const profileMetaData = await erc725js.getData();
      // Fetch all owned assets of the profile
        const receivedAssetsDataKey = await erc725js.fetchData('LSP5ReceivedAssets[]');
        console.log(receivedAssetsDataKey);
      console.log("profileMetaData", profileMetaData)

      if (
        profileMetaData.value &&
        typeof profileMetaData.value === 'object' &&
        'LSP3Profile' in profileMetaData.value
      ) {
        // Update the profile state
        return profileMetaData.value.LSP3Profile;
      }
    } catch (error) {
      console.log('Can not fetch profile data: ', error);
    }
  };