import invert from 'lodash/invert';

import { ChannelListTypes } from 'shared/constants';

export const InvitationShareModes = {
  EDIT: 'edit',
  VIEW_ONLY: 'view',
};

export const ChannelInvitationMapping = {
  [InvitationShareModes.EDIT]: ChannelListTypes.EDITABLE,
  [InvitationShareModes.VIEW_ONLY]: ChannelListTypes.VIEW_ONLY,
};

export const RouterNames = {
  CHANNELS_EDITABLE: 'CHANNELS_EDITABLE',
  CHANNELS_STARRED: 'CHANNELS_STARRED',
  CHANNELS_VIEW_ONLY: 'CHANNELS_VIEW_ONLY',
  CHANNELS_PUBLIC: 'CHANNELS_PUBLIC',
  CHANNEL_DETAILS: 'CHANNEL_DETAILS',
  CHANNEL_EDIT: 'CHANNEL_EDIT',
  CHANNEL_SETS: 'CHANNEL_SETS',
  CHANNEL_SET_DETAILS: 'CHANNEL_SET_DETAILS',
  CATALOG_ITEMS: 'CATALOG_ITEMS',
  CATALOG_DETAILS: 'CATALOG_DETAILS',
  CATALOG_FAQ: 'CATALOG_FAQ',
};

export const ListTypeToRouteMapping = {
  [ChannelListTypes.EDITABLE]: RouterNames.CHANNELS_EDITABLE,
  [ChannelListTypes.STARRED]: RouterNames.CHANNELS_STARRED,
  [ChannelListTypes.VIEW_ONLY]: RouterNames.CHANNELS_VIEW_ONLY,
  [ChannelListTypes.PUBLIC]: RouterNames.CHANNELS_PUBLIC,
};

export const RouteToListTypeMapping = invert(ListTypeToRouteMapping);
