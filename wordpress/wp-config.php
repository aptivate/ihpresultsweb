<?php
/**
 * The base configurations of the WordPress.
 *
 * This file has the following configurations: MySQL settings, Table Prefix,
 * Secret Keys, WordPress Language, and ABSPATH. You can find more information
 * by visiting {@link http://codex.wordpress.org/Editing_wp-config.php Editing
 * wp-config.php} Codex page. You can get the MySQL settings from your web host.
 *
 * This file is used by the wp-config.php creation script during the
 * installation. You don't have to use the web site, you can just copy this file
 * to "wp-config.php" and fill in the values.
 *
 * @package WordPress
 */

// ** MySQL settings - You can get this info from your web host ** //
/** The name of the database for WordPress */
define('DB_NAME', 'reactionscorecards3');

/** MySQL database username */
define('DB_USER', 'rs3_wp');

/** MySQL database password */
define('DB_PASSWORD', 'lz;smgrubmkcu,fy');

/** MySQL hostname */
define('DB_HOST', 'localhost');

/** Database Charset to use in creating database tables. */
define('DB_CHARSET', 'utf8');

/** The Database Collate type. Don't change this if in doubt. */
define('DB_COLLATE', '');

/**#@+
 * Authentication Unique Keys and Salts.
 *
 * Change these to different unique phrases!
 * You can generate these using the {@link https://api.wordpress.org/secret-key/1.1/salt/ WordPress.org secret-key service}
 * You can change these at any point in time to invalidate all existing cookies. This will force all users to have to log in again.
 *
 * @since 2.6.0
 */
define('AUTH_KEY',         '^&f8Tbgslm7rXjQJ#{v%{*g=$`;tuPCl!Be;|-Ogb[tg#45i[9t5A>{[w!WY[0(C');
define('SECURE_AUTH_KEY',  'HF;;]B)OpU.H|1q0rzqJ=Io!})W ~gDDpC^SmjsXc;Ni8m3o.QR:IH+u)qP>44|*');
define('LOGGED_IN_KEY',    ',Whys({;WJ r+.9,-(uza^+d14=ohoT[!zX#.Y8`&DjB^WC~]7=mF+t[Lz6nS~!L');
define('NONCE_KEY',        'j~)DV>+hBGT/Ze-JiqTP+>N4}xPrc73.-XY7@xGn&v=-|aJ1W+!ERNA8Uo@n]5^W');
define('AUTH_SALT',        'gIN`Q#wo JZuubw+3@sDK!c|~Y:{4^E8^<h@9*E+&I<|mwf0Tj!rsr;Y*hi0?u)r');
define('SECURE_AUTH_SALT', '`Bp8ak$0b^6}azBRW[0WF7+av-a$pe`+Aj:+9hw>7FOG#~Am,~z%E654gF]~&Z-+');
define('LOGGED_IN_SALT',   'U`ZCIW^ME`qBWm+2e;1@^*zCM(n[vT+QwOo)E9,9GV6[Nx`R+t >u0b!oqZ5ae==');
define('NONCE_SALT',       '(iTu>ZRQ1G+Q/K6n-T:|A||ZUW<Ds9bK5],5_CCKZfdHymoE/yppD+Z8;9v?F%1E');

/**#@-*/

/**
 * WordPress Database Table prefix.
 *
 * You can have multiple installations in one database if you give each a unique
 * prefix. Only numbers, letters, and underscores please!
 */
$table_prefix  = 'web_';

/**
 * WordPress Localized Language, defaults to English.
 *
 * Change this to localize WordPress.  A corresponding MO file for the chosen
 * language must be installed to wp-content/languages. For example, install
 * de.mo to wp-content/languages and set WPLANG to 'de' to enable German
 * language support.
 */
define ('WPLANG', '');

/**
 * For developers: WordPress debugging mode.
 *
 * Change this to true to enable the display of notices during development.
 * It is strongly recommended that plugin and theme developers use WP_DEBUG
 * in their development environments.
 */
define('WP_DEBUG', false);

/* That's all, stop editing! Happy blogging. */

/** Absolute path to the WordPress directory. */
if ( !defined('ABSPATH') )
	define('ABSPATH', dirname(__FILE__) . '/');

/** Sets up WordPress vars and included files. */
require_once(ABSPATH . 'wp-settings.php');
