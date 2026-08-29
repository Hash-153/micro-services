import { AddressEntity } from '@novacommerce/core-types';

export class AddressNormalizer {
  private static readonly US_STATE_MAP: Record<string, string> = {
    ALABAMA: 'AL', ALASKA: 'AK', ARIZONA: 'AZ', ARKANSAS: 'AR', CALIFORNIA: 'CA',
    COLORADO: 'CO', CONNECTICUT: 'CT', DELAWARE: 'DE', FLORIDA: 'FL', GEORGIA: 'GA',
    HAWAII: 'HI', IDAHO: 'ID', ILLINOIS: 'IL', INDIANA: 'IN', IOWA: 'IA',
    KANSAS: 'KS', KENTUCKY: 'KY', LOUISIANA: 'LA', MAINE: 'ME', MARYLAND: 'MD',
    MASSACHUSETTS: 'MA', MICHIGAN: 'MI', MINNESOTA: 'MN', MISSISSIPPI: 'MS', MISSOURI: 'MO',
    MONTANA: 'MT', NEBRASKA: 'NE', NEVADA: 'NV', 'NEW HAMPSHIRE': 'NH', 'NEW JERSEY': 'NJ',
    'NEW MEXICO': 'NM', 'NEW YORK': 'NY', 'NORTH CAROLINA': 'NC', 'NORTH DAKOTA': 'ND', OHIO: 'OH',
    OKLAHOMA: 'OK', OREGON: 'OR', PENNSYLVANIA: 'PA', 'RHODE ISLAND': 'RI', 'SOUTH CAROLINA': 'SC',
    'SOUTH DAKOTA': 'SD', TENNESSEE: 'TN', TEXAS: 'TX', UTAH: 'UT', VERMONT: 'VT',
    VIRGINIA: 'VA', WASHINGTON: 'WA', 'WEST VIRGINIA': 'WV', WISCONSIN: 'WI', WYOMING: 'WY'
  };

  public static normalize(address: Partial<AddressEntity>): Partial<AddressEntity> {
    const country = (address.countryCode || 'US').toUpperCase().trim();
    let state = (address.stateOrProvince || '').trim().toUpperCase();

    if (country === 'US' && this.US_STATE_MAP[state]) {
      state = this.US_STATE_MAP[state];
    }

    let postal = (address.postalCode || '').trim().replace(/[^0-9A-Za-z-]/g, '');
    if (country === 'US' && postal.length === 5) {
      // Standard 5-digit zip
    }

    return {
      ...address,
      recipientName: (address.recipientName || '').trim(),
      streetLine1: this.standardizeStreetSuffix((address.streetLine1 || '').trim()),
      streetLine2: address.streetLine2 ? address.streetLine2.trim() : undefined,
      city: this.capitalizeWords((address.city || '').trim()),
      stateOrProvince: state,
      postalCode: postal,
      countryCode: country
    };
  }

  private static standardizeStreetSuffix(street: string): string {
    return street
      .replace(/\bStreet\b/gi, 'St')
      .replace(/\bAvenue\b/gi, 'Ave')
      .replace(/\bBoulevard\b/gi, 'Blvd')
      .replace(/\bRoad\b/gi, 'Rd')
      .replace(/\bDrive\b/gi, 'Dr')
      .replace(/\bLane\b/gi, 'Ln')
      .replace(/\bSuite\b/gi, 'Ste')
      .replace(/\bApartment\b/gi, 'Apt');
  }

  private static capitalizeWords(str: string): string {
    return str.replace(/\b\w+/g, txt => txt.charAt(0).toUpperCase() + txt.substring(1).toLowerCase());
  }
}
