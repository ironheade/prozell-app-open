import React from 'react';
import {
  Header,
  HeaderContainer,
  HeaderName,
  HeaderNavigation,
  HeaderMenuButton,
  HeaderMenuItem,
  HeaderGlobalBar,
  HeaderGlobalAction,
  SkipToContent,
  SideNav,
  SideNavItems,
  HeaderSideNavItems,
} from 'carbon-components-react';
import { Basketball24, Apple24, UserAvatar24 } from '@carbon/icons-react';
import { Link } from 'react-router-dom';

const TutorialHeader = () => (
  <HeaderContainer
    render={({ isSideNavExpanded, onClickSideNavExpand }) => (
      <Header aria-label="Carbon Tutorial">
        <SkipToContent />
        <HeaderMenuButton
          aria-label="Open menu"
          isCollapsible
          onClick={onClickSideNavExpand}
          isActive={isSideNavExpanded}
        />
        <HeaderName element={Link} to="/" prefix="IPAT">
          ProZell Kostenrechner
        </HeaderName>
        <HeaderNavigation aria-label="Carbon Tutorial">
          <HeaderMenuItem element={Link} to="/Zellauslegung">
            Zellauslegung
          </HeaderMenuItem>
          <HeaderMenuItem element={Link} to="/Prozessauslegung">
            Prozessauslegung
          </HeaderMenuItem>
          <HeaderMenuItem element={Link} to="/AllgemeineParameter">
            Allgemeine Parameter
          </HeaderMenuItem>
          <HeaderMenuItem element={Link} to="/Ergebnisse">
            Ergebnisse
          </HeaderMenuItem>
        </HeaderNavigation>
        <SideNav
          aria-label="Side navigation"
          expanded={isSideNavExpanded}

          isPersistent={false}
          >
          <SideNavItems>
            <HeaderSideNavItems>
              <HeaderMenuItem element={Link} to="/">
                Startseite
              </HeaderMenuItem>
              <HeaderMenuItem element={Link} to="/Zellauslegung">
                Zellauslegung
              </HeaderMenuItem>
              <HeaderMenuItem element={Link} to="/Prozessauslegung">
                Prozessauslegung
              </HeaderMenuItem>
              <HeaderMenuItem element={Link} to="/AllgemeineParameter">
                Allgemeine Parameter
              </HeaderMenuItem>
              <HeaderMenuItem element={Link} to="/Ergebnisse">
                Ergebnisse
              </HeaderMenuItem>
            </HeaderSideNavItems>
          </SideNavItems>
        </SideNav>
        <HeaderGlobalBar>
          <HeaderGlobalAction aria-label="Notifications">
            <Apple24 />
          </HeaderGlobalAction>
          <HeaderGlobalAction aria-label="User Avatar">
            <UserAvatar24 />
          </HeaderGlobalAction>
          <HeaderGlobalAction aria-label="App Switcher">
            <Basketball24 />
          </HeaderGlobalAction>
        </HeaderGlobalBar>
      </Header>
    )}
  />
);

export default TutorialHeader;
